import generators as g
import datetime as d
import random as r


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
               self.imie +'","' + self.nazwisko +'","' + str(self.data_urodzenia) + '","' + str(self.data_przyjecia) + '","' + self.plec + '","' + self.pesel + '"'

class Wizyta:
    n = 0
    def __init__(self, pacjent: Pacjent, time_1, time_2):
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
        self.diagnoza: Diagnoza = Diagnoza()


    def addPacjent(self, pacjent: Pacjent):
        self.pacjent = pacjent

    def toSQL(self):
            return 'insert into Wizyty (id, data, czy_sie_stawil, czy_wyleczony, koszt, ocena, pacjent, reklamacja, diagnoza) values "' + str(self.id) + '","' +\
                   str(self.data) + '","' + str(self.czy_sie_stawil) + '","' + str(self.czy_wyleczony) + '","' + str(self.koszt) + '","' + str(self.ocena) + '","' + \
                str(self.pacjent.pesel) + '","' + str(self.diagnoza.id) + '","' + (str(self.reklamacja.id) if self.reklamacja != None else ' ') + '"'


class Reklamacja:
    n=0
    def __init__(self, wiz: Wizyta):
        self.id = Wizyta.n
        Wizyta.n+=1
        self.tresc = g.generate_reklamacja_tresc()
        self.czy_uznano = r.randint(0,1)
        self.wizyta = wiz
        self.data_reklamacji = g.generate_date(self.wizyta.data,self.wizyta.data)

    def addWizyta(self, wizyta: Wizyta):
        self.wizyta = wizyta
        #self.data_reklamacji = Wizyta

    def toSQL(self):
        return 'insert into Reklamacje (tresc, czy_uznano, wizyta, data_reklamacji) values "' + \
               str(
                   self.data) + '","' + self.czy_sie_stawil + '","' + self.czy_wyleczony + '","' + self.koszt + '","' + self.ocena + '","' + \
               self.pacjent.pesel + '","' + self.diagnoza.id + '","' + self.reklamacja.id + '"'


class Diagnoza:
    n=0
    def __init__(self):
        self.id = Diagnoza.n
        Diagnoza.n +=1
        pass




class Lekarz:
    def __init__(self):
        self.imie = g.generate_first_name()
        self.nazwisko = g.generate_last_name()
        self.data_urodzenia = g.generate_date(d.date(1950, 1, 1), d.date(1970, 12, 31))
        self.PESEL = g.generate_pesel(self.data_urodzenia)






class Lek:
    def __init__(self):
        pass

class Skierowanie:
    def __init__(self):
        pass

class Skierowanie_na_zabieg:
    def __init__(self):
        pass

class Sprzet:
    def __init__(self):
        pass

class Zabieg:
    def __init__(self):
        pass
