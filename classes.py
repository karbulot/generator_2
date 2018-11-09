import generators as g
import datetime as d
import random as r
#import main as m

class Lekarz:
    def __init__(self, time_1, specj):
        self.imie = g.generate_first_name()
        self.nazwisko = g.generate_last_name()
        self.data_urodzenia = g.generate_date(d.date(1950, 1, 1), d.date(1970, 12, 31))
        self.data_przyjecia = g.generate_date(time_1 - d.timedelta(days=365), time_1)
        self.PESEL = g.generate_pesel(self.data_urodzenia)
        self.specjalizacja = g.generate_specjalizacja() if specj == None else specj
    def toSQL(self):
        return 'insert into Lekarze (imie, nazwisko, data_urodzenia, pesel, specjalizacja) values "' + \
                '","' + self.imie + '","' + self.nazwisko + str(self.data_urodzenia) +'","' + self.pesel + '","' + self.specjalizacja + '";'


class Pacjent:
    def __init__(self, time_1, time_2):
        self.imie = g.generate_first_name()
        self.nazwisko = g.generate_last_name()
        self.data_urodzenia = g.generate_date(d.date(1950,1,1),d.date(1970,12,31))
        self.data_przyjecia = g.generate_date(time_1,time_2)
        self.plec = 'F' if self.imie[1:] == 'a' else 'M'
        self.pesel = g.generate_pesel(self.data_urodzenia)

    def toSQL(self):
        return 'insert into Pacjenci (imie, nazwisko, data_urodzenia, data_przyjecia, plec, pesel) values "' + \
               self.imie +'","' + self.nazwisko +'","' + str(self.data_urodzenia) + '","' + str(self.data_przyjecia) + '","' + self.plec + '","' + self.pesel + '";'


class Wizyta:
    n = 0
    def __init__(self, pacjent: Pacjent, time_1, time_2, lekarze, leki):
        self.id = Wizyta.n
        Wizyta.n+=1
        self.czy_wyleczony = r.randint(0,1)
        self.czy_sie_stawil = r.randint(0,5)
        if self.czy_sie_stawil > 0:
            self.czy_sie_stawil = 1
        self.ocena = r.randint(1,5)
        self.koszt = r.randint(5,50) * 10
        self.pacjent: Pacjent = pacjent
        self.data = g.generate_date(pacjent.data_przyjecia, time_2)
        self.reklamacja: Reklamacja = Reklamacja(self) if r.randint(0,5) > 3 else None
        self.diagnoza: Diagnoza = Diagnoza(lekarze, leki, self, self.czy_wyleczony)


    def addPacjent(self, pacjent: Pacjent):
        self.pacjent = pacjent

    def toSQL(self):
            return 'insert into Wizyty (id, data, czy_sie_stawil, czy_wyleczony, koszt, ocena, pacjent, reklamacja, diagnoza) values "' + str(self.id) + '","' +\
                   str(self.data) + '","' + str(self.czy_sie_stawil) + '","' + str(self.czy_wyleczony) + '","' + str(self.koszt) + '","' + str(self.ocena) + '","' + \
                str(self.pacjent.pesel) + '","' + str(self.diagnoza.id) + '","' + ('' if self.reklamacja is None else str(self.reklamacja.id)) + '";'


class Reklamacja:
    n = 0
    def __init__(self, wiz: Wizyta):
        self.id = Reklamacja.n
        Reklamacja.n +=1
        self.tresc = g.generate_reklamacja_tresc()
        self.czy_uznano = r.randint(0,1)
        self.wizyta = wiz
        self.data_reklamacji = g.generate_date(self.wizyta.data,self.wizyta.data + d.timedelta(days=5))

    def addWizyta(self, wizyta: Wizyta):
        self.wizyta = wizyta
        #self.data_reklamacji = Wizyta

    def toSQL(self):
        return 'insert into Reklamacje (id, tresc, czy_uznano, wizyta, data_reklamacji) values "' + \
               str(self.id) + '","' + self.tresc + '","' + str(self.czy_uznano) + '","' + str(self.wizyta.id) + '","' + str(self.data_reklamacji) + '";'


class Diagnoza:
    n=0
    def __init__(self, lekarze, leki, wizyta: Wizyta, czy_wyleczony):
        self.id = Diagnoza.n
        Diagnoza.n +=1
        self.choroba = g.generate_illness()
        self.lekarz: Lekarz = g.choose_doctor(lekarze, self.choroba)
        self.lek: Lek = g.choose_lek(leki, self.choroba)
        self.wizyta = wizyta
        self.skierowanie = Skierowanie(self)
        pass
    def toSQL(self):
        return 'insert into Diagnozy (id, choroba, lekarz, skierowanie) values "' + \
               str(self.id) + '","' + self.choroba + '","' + self.czy_wyleczony + '","' + self.koszt + '","' + self.ocena + '","' + \
               self.pacjent.pesel + '","' + self.diagnoza.id + '","' + self.reklamacja.id + '","'+ self.skierowanie.id+ '";'





class Lek:
    n = 0
    def __init__(self):
        self.id = Lek.n
        Lek.n+=1
        self.producent = r.choice(list(open('LekiKoniec.txt')))[:-1]
        self.nazwa = r.choice(list(open('LekiPoczatek.txt')))[:-1] + self.producent
        self.producent += "pol"
        self.producent.capitalize()
        self.dawkowanie = str(r.randint(1,4)) + " razy dziennie przez " + str(r.randint(2,4)) + " tygodnie "
        self.choroba = g.generate_illness()

    def toSQL(self):
        return 'insert into Leki (id, producent, nazwa, dawkowanie) values "' + \
               str(self.id) + '","' + self.producent + '","' + self.nazwa + '","' + self.dawkowanie + '";'


class Skierowanie:
    n = 0
    def __init__(self, diagnoza: Diagnoza):
        self.id = Skierowanie.n
        Skierowanie.n +=1
        self.tresc = g.generate_skierowanie_tresc()
        self.zabiegi = []
        self.diagnoza = diagnoza
        for i in range(2,5):
            self.zabiegi.append(Skierowanie_na_zabieg(self, diagnoza.wizyta))
    def toSQL(self):
        return 'insert into Skierowania (id, tresc, diagnoza) values "' + \
               str(self.id) + '","' + self.tresc + '","' + self.diagnoza.id + '";'

class Skierowanie_na_zabieg:
    n = 0
    def __init__(self, skierowanie: Skierowanie, wizyta: Wizyta):
        self.id = Skierowanie_na_zabieg.n
        Skierowanie_na_zabieg.n += 1
        self.liczba_zabiegow = r.randint(1,8)
        self.sprzet = Sprzet()
        self.skierowanie = skierowanie
        self.zabiegi = []
        for i in range(self.liczba_zabiegow):
            self.zabiegi.append(Zabieg(wizyta,self))
    def toSQL(self):
        return 'insert into Skierowania_na_zabieg (id, liczba_zabiegow, sprzet, skierowanie) values "' + \
               str(self.id) + '","' + self.liczba_zabiegow + '","' + self.sprzet.id + '","' + self.skierowanie.id + '";'

class Sprzet:
    n = 0
    def __init__(self):
        self.id = Sprzet.n
        Sprzet.n += 1
        self.nazwa = g.generate_sprzet_name()
        self.typ = g.generate_specjalizacja()
    def toSQL(self):
        return 'insert into Sprzety (id, nazwa, typ) values "' + \
               str(self.id) + '","' + self.nazwa + '","' + self.typ + '";'


class Zabieg:
    def __init__(self, wizyta: Wizyta, skierowanie_na_zabieg: Skierowanie_na_zabieg):
        self.data_wykonania = g.generate_date(wizyta.data,wizyta.data + d.timedelta(days=30))
        self.rezultat = "ok" if r.randint(0,300) != 5 else "nie powiódł się"
        self.skierowanie_na_zabieg = skierowanie_na_zabieg.skierowanie
    def toSQL(self):
        return 'insert into Zabiegi (data_wykonania, rezultat, skierowanie_na_zabieg) values "' + \
               str(self.data_wykonania) + '","' + self.rezultat + '","' + str(self.skierowanie_na_zabieg.id) + '";'
