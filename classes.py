import generators as g
import datetime as d
import random as r

class Pacjent:
    def __init__(self, time_1, time_2):
        self.imie = g.generate_first_name()
        self.nazwisko = g.generate_last_name()
        self.data_urodzenia = g.generate_date(d.date(1950,1,1),d.date(1970,12,31))
        self.data_przyjecia = g.generate_date(time_1,time_2)
        self.PESEL = g.generate_pesel(self.data_urodzenia)

class Lekarz:
    def __init__(self):
        self.imie = g.generate_first_name()
        self.nazwisko = g.generate_last_name()
        self.PESEL = g.generate_pesel(self.data_urodzenia)

class Wizyta:
    def __init__(self, pacjent: Pacjent):
        self.czy_wyleczony = r.randint(0,1)
        self.czy_sie_stawil = r.randint(0,5)
        if self.czy_sie_stawil > 0:
            self.czy_sie_stawil = 1
        self.ocena = r.randint(1,5)
        self.koszt = r.randint(5,50) * 10
        self.pacjent = pacjent
        self.reklamacja = None
        self.diagnoza = None
        self.data = g.generate_date()

    def addPacjent(self, pacjent: Pacjent):
        self.pacjent = pacjent


class Reklamacja:
    def __init__(self):
        self.tresc = g.generate_reklamacja_tresc()
        self.czy_uznano = r.randint(0,1)
        self.wizyta = None
        self.data_reklamacji = None

    def addWizyta(self, wizyta: Wizyta):
        self.wizyta = wizyta
        #self.data_reklamacji = Wizyta

class Diagnoza:
    def __init__(self):
        pass

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
