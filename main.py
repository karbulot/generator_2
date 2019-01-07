import classes as c
import datetime as d


N_PACJENT = 30
N_LEKARZ = 10
N_LEK = 25
N_SPRZET = 50


T_1 = d.date(2016,1,1)
T_2 = d.date(2017,1,1)
T_3 = d.date(2018,1,1)
T_4 = d.date(2019,1,1)

class Things:
    def __init__(self,filename):
        self.Pacjenci = []
        self.Wizyty = []
        self.Dawkowania = []
        self.Reklamacje = []
        self.Lekarze = []
        self.Diagnozy = []
        self.Recepty = []
        self.Skierowania = []
        self.Sprzety = []
        self.Skierowanianazabiegi = []
        self.Zabiegi = []
        self.Godziny = []
        self.Daty = []
        self.filename = filename
        self.file_object = open(filename, "w")

    def iter(self):
        return [self.Pacjenci, self.Lekarze, self.Reklamacje, self.Diagnozy, self.Recepty, self.Sprzety, self.Godziny,
                self.Daty, self.Skierowania,
                #self.Skierowanianazabiegi,
                self.Zabiegi, self.Dawkowania, self.Wizyty]

    def toSQL(self):
        self.Lekarze.sort(key=lambda x: x.id)
        self.file_object = open(self.filename, "w")
        for i in self.iter():
            for element in i:
                self.file_object.write(element.toSQL())
                self.file_object.write('\n')
        self.file_object.close()

things1 = Things("insert1.sql")

"""
Pacjenci2 = []
Wizyty2 = []
Reklamacje2 = []
Lekarze2 = []
Diagnozy2 = []
Leki2 = []
Skierowania2 = []
Sprzety2 = []
Skierowanianazabiegi2 = []
Zabiegi2 = []

Pacjenci3 = []
Wizyty3 = []
Reklamacje3 = []
Lekarze3 = []
Diagnozy3 = []
Leki3 = []
Skierowania3 = []
Sprzety3 = []
Skierowanianazabiegi3 = []
Zabiegi3 = []
"""
#print(c.g.generate_pesel(d.date(1945,1,1)))



def generate_doctors(doctors, n: int):

    for i in range (n):
        doctors.append(c.Lekarz(T_1, None, doctors))

def generate_hours(godziny: list):
    for i in range(24):
        for j in range(60):
            godziny.append(c.Godzina(j,i))
    return godziny

def generate_dates(daty: list, t_1, t_2):
    for j in [d.date.fromordinal(i) for i in range(t_1.toordinal(),t_2.toordinal())]:
        daty.append(c.Data(j))
    return daty

#def generate_dates(daty: list, rok):
#    for i in range()

def first_point_in_time(t: Things):
    #Lekarze:
    generate_hours(t.Godziny)
    generate_dates(t.Daty, T_1, T_2)
    generate_doctors(t.Lekarze,N_LEKARZ)

    t.Lekarze.append(c.Lekarz(T_1,"Kardiolog", t.Lekarze))
    t.Lekarze.append(c.Lekarz(T_1,"Psychiatra", t.Lekarze))
    t.Lekarze.append(c.Lekarz(T_1,"Laryngolog", t.Lekarze))
    t.Lekarze.append(c.Lekarz(T_1,"Anestezjolog", t.Lekarze))
    t.Lekarze.append(c.Lekarz(T_1,"Okulista", t.Lekarze))
    t.Lekarze.append(c.Lekarz(T_1,"Neurolog", t.Lekarze))
    t.Lekarze.append(c.Lekarz(T_1,"Onkolog", t.Lekarze))
    t.Lekarze.sort(key=lambda x: x.id)
    #leki, sprzęty
    #for i in range(N_LEK):
    #    t.Leki.append(c.Recepta())
    for i in range(N_SPRZET):
        t.Sprzety.append(c.Sprzet())

    # Pacjenci, Wizyty, Reklamacje, Diagnozy, Skierowania, Skierowania na Zabieg, Zabiegi
    for i in range(N_PACJENT):
        t.Pacjenci.append(c.Pacjent(T_1, T_2))
    for i in t.Pacjenci:
        #print(i.toSQL())
        for j in range(0,c.r.randint(1,10)):
            wizyta_temp = c.Wizyta(i,T_1,T_2, t.Lekarze, t.Recepty, t.Sprzety)
            t.Wizyty.append(wizyta_temp)
            #print(wizyta_temp.toSQL())
    for wiz in t.Wizyty:
        if wiz.reklamacja is not None:
            t.Reklamacje.append(wiz.reklamacja)
        t.Diagnozy.append(wiz.diagnoza)
        t.Recepty.append(wiz.recepta)
        t.Skierowania.append(wiz.skierowanie)


    for skier in t.Skierowania:
        for zab in skier.zabiegi:
            #t.Skierowanianazabiegi.append(zab)
            for zabb in zab.zabiegi:
                t.Zabiegi.append(zabb)

    for rec in t.Recepty:
        t.Dawkowania.append(rec.dawkowanie)


#things2 = things1


def next_point_in_time(t: Things,t_1,t_2,n_new_doctors, n_new_patients, n_patients_left):
    #date_range = [d.date.fromordinal(i) for i in range(t_1.toordinal(),t_2.toordinal())]
    generate_dates(t.Daty, t_1, t_2)
    c.r.shuffle(t.Pacjenci)
    #t.Pacjenci = t.Pacjenci[n_patients_left:]
    generate_doctors(t.Lekarze, n_new_doctors)
    nowe_wizyty = []
    nowi_pacjenci = []
    nowe_recepty = []
    for i in range(n_new_patients):
        nowi_pacjenci.append(c.Pacjent(t_1, t_2))
    for i in nowi_pacjenci:
        for j in range(0,c.r.randint(1,10)):
            wizyta_temp = c.Wizyta(i,t_1,t_2, t.Lekarze, t.Recepty, t.Sprzety)
            nowe_wizyty.append(wizyta_temp)
    t.Pacjenci+=nowi_pacjenci
    for i in range(N_SPRZET):
        t.Sprzety.append(c.Sprzet())

    # Pacjenci, Wizyty, Reklamacje, Diagnozy, Skierowania, Skierowania na Zabieg, Zabiegi
    for wiz in nowe_wizyty:
        if wiz.reklamacja is not None:
            t.Reklamacje.append(wiz.reklamacja)
        t.Diagnozy.append(wiz.diagnoza)
        nowe_recepty.append(wiz.recepta)
        t.Skierowania.append(wiz.skierowanie)
    t.Wizyty+=nowe_wizyty

    for skier in t.Skierowania:
        for zab in skier.zabiegi:
            for zabb in zab.zabiegi:
                t.Zabiegi.append(zabb)

    for rec in nowe_recepty:
        t.Dawkowania.append(rec.dawkowanie)

    t.Recepty+=nowe_recepty


    return t


first_point_in_time(things1)
things1.toSQL()
print("dfgdsfg")
#things2 = things1
things1.filename = "insert2.sql"
next_point_in_time(things1,T_2,T_3,10,10,5)
print("dfgdsgf")
things1.toSQL()
#things3 = things2
things1.filename = "insert3.sql"
next_point_in_time(things1,T_3,T_4,10,10,5)
print("fdgdfg")
things1.toSQL()