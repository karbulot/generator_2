import generators as g
import datetime as d
import random as r

class Lekarz:
    n = 0

    def __init__(self, time_1, specj, lekarze):
        self.id = Lekarz.n
        Lekarz.n += 1
        self.imie_i_nazwisko: str = g.generate_first_name() + " " + g.generate_last_name()
        self.data_urodzenia = g.generate_date(d.date(1950, 1, 1), d.date(1970, 12, 31))
        self.data_przyjecia = g.generate_date(time_1 - d.timedelta(days=365), time_1)
        self.pesel = g.generate_pesel(self.data_urodzenia)
        self.specjalizacja = g.generate_specjalizacja() if specj is None else specj
        self.stanowisko: int = r.randint(1,3)
        self.zwierzchnik: Lekarz = g.choose_doctor3(lekarze, self.stanowisko)
        self.aktualnosc = True

    def toSQL(self):
        return "insert into Lekarze (id, imie_i_nazwisko,  pesel, specjalizacja, stanowisko, zwierzchnik, aktualnosc)" \
               " values ('" + str(self.id) + "','" \
               + self.imie_i_nazwisko + "','" + self.pesel + "','" + self.specjalizacja + "','"\
               + g.get_stanowisko(self.stanowisko) + "'," + ("null" if self.zwierzchnik is None else "'" + str(self.zwierzchnik.id) + "'") + ",'" + str(self.aktualnosc) + "');"


class Pacjent:
    n = 0

    def __init__(self, time_1, time_2):
        self.id = Pacjent.n
        Pacjent.n += 1
        self.imie = g.generate_first_name()
        self.imie_i_nazwisko =  self.imie + " " + g.generate_last_name()
        self.data_urodzenia = g.generate_date(d.date(1950,1,1),d.date(1970,12,31))
        self.data_przyjecia = g.generate_date(time_1,time_2)
        self.plec = "F" if self.imie_i_nazwisko[1:] == "a" else "M"
        self.pesel = g.generate_pesel(self.data_urodzenia)
        self.aktualnosc = 'true'

    def toSQL(self):
        return "insert into Pacjenci (id, imie_i_nazwisko, data_urodzenia, data_przyjecia, plec, pesel, aktualnosc) values ('" + \
               str(self.id) + "','" + self.imie_i_nazwisko +"','" + str(self.data_urodzenia) + "','" + str(self.data_przyjecia) + "','" + self.plec + "','" + self.pesel + "','" + self.aktualnosc + "');"


class Wizyta:
    n = 0
    def __init__(self, pacjent: Pacjent, time_1, time_2, lekarze, leki, sprzety):
        self.id = Wizyta.n
        Wizyta.n+=1
        self.czy_wyleczony = r.randint(0,1)
#        self.czy_sie_stawil = r.randint(0,5)
#        if self.czy_sie_stawil > 0:
#            self.czy_sie_stawil = 1
        self.ocena = r.randint(1,5)
        self.oplata = r.randint(5,50) * 10
        self.pacjent: Pacjent = pacjent
        self.data = g.generate_date(pacjent.data_przyjecia, time_2)
        self.reklamacja: Reklamacja = Reklamacja(self) if r.randint(0,5) > 3 else None
        self.diagnoza: Diagnoza = Diagnoza(lekarze, leki, self, self.czy_wyleczony)
        self.lekarz =  self.diagnoza.lekarz
        self.godzina = g.generate_hour()
        self.skierowanie = Skierowanie(self.diagnoza, lekarze, sprzety)
        self.numer_wizyty = g.gen_numerwizyty()
        self.recepta: Recepta = Recepta(pacjent)


    def addPacjent(self, pacjent: Pacjent):
        self.pacjent = pacjent

    def toSQL(self):
            return "insert into Wizyty (data, godzina, pacjent, skierowanie, reklamacja, diagnoza, recepta, ocena, " \
                   "oplata, numer_wizyty) values ('"+\
                   str(self.data) + "','" + str(self.godzina) + "','" + str(self.pacjent.id) + "','" + \
                   str(self.skierowanie.id) + \
                   "'," + ("null" if self.reklamacja is None else "'"+ str(self.reklamacja.id) + "'") + \
                ",'" + str(self.diagnoza.id) + "','" + str(self.recepta.id) + "','" + str(self.ocena) +  \
                   "','" + str(self.oplata) + "','" + str(self.numer_wizyty) + "');"


class Reklamacja:
    n = 0
    def __init__(self, wiz: Wizyta):
        self.id = Reklamacja.n
        Reklamacja.n +=1
        #self.tresc = g.generate_reklamacja_tresc()
        self.czy_uznano = r.randint(0,1)
        self.typ: str = r.choice(['Nieudany zabieg','Zła diagnoza','Skarga na personel'])
        #self.wizyta = wiz
        #self.data_reklamacji = g.generate_date(self.wizyta.data,self.wizyta.data + d.timedelta(days=5))

    def addWizyta(self, wizyta: Wizyta):
        self.wizyta = wizyta
        #self.data_reklamacji = Wizyta

    def toSQL(self):
        return "insert into Reklamacje (id, czy_uznano, typ) values ('" + \
               str(self.id) + "','" + str(self.czy_uznano) + "','" + str(self.typ) + "');"


class Diagnoza:
    n=0
    def __init__(self, lekarze, leki, wizyta: Wizyta, czy_wyleczony):
        self.id = Diagnoza.n
        Diagnoza.n +=1
        self.choroba: str = g.generate_illness()
        self.lekarz: Lekarz = g.choose_doctor(lekarze, self.choroba)
        #self.lek: Lek = g.choose_lek(leki, self.choroba)
        self.wizyta = wizyta
        #self.skierowanie = Skierowanie(self, lekarze)
        #pass
    def toSQL(self):
        return "insert into Diagnozy (id, choroba) values ('" + \
               str(self.id) + "','" + self.choroba + "');"


class Recepta:
    n = 0
    def __init__(self, pacjent):
        self.id = Recepta.n
        Recepta.n+=1
        self.producent = r.choice(list(open("LekiKoniec.txt")))[:-1]
        self.nazwa = r.choice(list(open("LekiPoczatek.txt")))[:-1] + self.producent
        self.producent += 'pol'
        self.producent.capitalize()
        self.dawkowanie = Dawkowanie(self, pacjent)
        #self.dawkowanie = str(r.randint(1,4)) + ' razy dziennie przez ' + str(r.randint(2,4)) + ' tygodnie '
        #self.choroba = g.generate_illness()

    def toSQL(self):
        return "insert into Recepty (id, producent, nazwa) values ('" + \
               str(self.id) + "','" + self.producent + "','" + self.nazwa + "');"


class Skierowanie:
    n = 0
    def __init__(self, diagnoza: Diagnoza, lekarze, sprzety):
        self.id = Skierowanie.n
        Skierowanie.n +=1
        self.typ = r.choice(['pilne','zwykle'])
        #self.tresc = g.generate_skierowanie_tresc()
        self.zabiegi = []
        self.diagnoza = diagnoza
        for i in range(2,5):
            self.zabiegi.append(Skierowanie_na_zabieg(self, diagnoza.wizyta, lekarze, sprzety))
    def toSQL(self):
        return "insert into Skierowania (id, typ) values ('" + \
               str(self.id) + "','" + self.typ + "');"

class Skierowanie_na_zabieg:
    n = 0
    def __init__(self, skierowanie: Skierowanie, wizyta: Wizyta, lekarze, sprzety: list):
        self.id = Skierowanie_na_zabieg.n
        Skierowanie_na_zabieg.n += 1
        self.liczba_zabiegow = r.randint(1,8)
        self.sprzet = g.choose_sprzet(sprzety, skierowanie.diagnoza.lekarz.specjalizacja)
        self.skierowanie = skierowanie
        self.zabiegi = []
        self.wizyta = wizyta
        for i in range(self.liczba_zabiegow):
            self.zabiegi.append(Zabieg(wizyta,self, lekarze))
    def toSQL(self):
        return "insert into Skierowania_na_zabieg (id, liczba_zabiegow, sprzet, skierowanie) values ('" + \
               str(self.id) + "','" + str(self.liczba_zabiegow) + "','" + str(self.sprzet.id) + "','" + str(self.skierowanie.id) + "');"

class Sprzet:
    n = 0
    def __init__(self):
        self.id = Sprzet.n
        Sprzet.n += 1
        self.nazwa = g.generate_sprzet_name()
        self.typ = g.generate_specjalizacja()
    def toSQL(self):
        return "insert into Sprzety (id, nazwa, typ) values ('" + \
               str(self.id) + "','" + self.nazwa + "','" + self.typ + "');"


class Zabieg:
    def __init__(self, wizyta: Wizyta, skierowanie_na_zabieg: Skierowanie_na_zabieg, lekarze):
        self.data_wykonania = g.generate_date(wizyta.data,wizyta.data + d.timedelta(days=30))
        self.godzina = g.generate_hour()
        self.rezultat = 'ok' if r.randint(0,300) != 5 else 'nie powiódł się'
        self.skierowanie: Skierowanie = skierowanie_na_zabieg.skierowanie
        self.lekarz = g.choose_doctor2(lekarze,skierowanie_na_zabieg.sprzet.typ)
        self.lekarz_wyk = g.choose_doctor2(lekarze,skierowanie_na_zabieg.sprzet.typ)
        self.poruszanie_konczynami = r.randint(0,2)
        self.oddech = r.randint(0,2)
        self.krazenie = r.randint(0,2)
        self.stan_przytomnosci =r.randint(0,2)
        self.kolor_skory = r.randint(0,2)
        self.sprzet = skierowanie_na_zabieg.sprzet.id
        self.pacjent = skierowanie_na_zabieg.wizyta.pacjent

    def toSQL(self):
        return "insert into Zabiegi (data_wykonania, lekarz_wykonujacy, lekarz_zlecajacy, pacjent, sprzet, " \
               "poruszanie_konczynami, oddech, krazenie, stan_przytomnosci, kolor_skory, godzina, skierowanie) values ('" + \
               str(self.data_wykonania) + "','" \
               + str(self.lekarz_wyk.id) + "','" \
               + str(self.lekarz.id) + "','" \
               + str(self.pacjent.id) + "','" \
        + str(self.sprzet) + "','" \
        + str(self.poruszanie_konczynami) + "','" \
        + str(self.oddech) + "','" \
        + str(self.krazenie) + "','" \
        + str(self.stan_przytomnosci) + "','" \
        + str(self.kolor_skory)+ "','" \
        + str(self.godzina) + "','" \
        + str(self.skierowanie.id) + "');"

class Godzina:
    n = 0
    def __init__(self, minuta, godzina):
        self.id: int = Godzina.n
        Godzina.n += 1
        self.minuta: str = minuta
        self.godzina: str = godzina

    def toSQL(self):
         return "insert into Godziny(id, godzina, minuta) values ('" + \
               str(self.id) + "','" \
               + str(self.godzina) + "','" \
               + str(self.minuta) + \
               "');"

class Data:
    n=0
    def __init__(self, dzien, miesiac, rok):
        self.id: int = Data.n
        Data.n += 1
        self.dzien: str = dzien
        self.miesiac: str = miesiac
        self.rok: str = rok

    def toSQL(self):
        return "insert into Daty(id, rok, miesiac, dzien) values ('" + \
               str(self.id) + "','" \
               + self.rok + "','" \
               + str(self.miesiac) + "','" \
               + self.dzien + \
               "');"

class Dawkowanie:
    def __init__(self, recepta: Recepta, pacjent: Pacjent):
        self.numer_recepty = g.gen_numerwizyty()
        self.dawka = r.choice([100,200,300,400,500])
        self.ile = r.randint(1,5)
        self.liczba_dni = r.choice([7,14,21,28])
        self.data = g.generate_date()
        self.pacjent = pacjent
        self.recepta = recepta

    def toSQL(self):
        return "insert into Dawkowania(pacjent, recepta, ile_razy_dziennie, dawka, nr_recepty, liczba_dni) values ('" + \
               str(self.pacjent.id) + "','" \
               + str(self.recepta.id) + "','" \
               + str(self.ile) + "','" \
               + str(self.dawka) + "','" \
               + str(self.numer_recepty) + "','" \
                + str(self.liczba_dni) + "');'"
