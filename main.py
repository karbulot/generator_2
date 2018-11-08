import classes as c
import datetime as d


N_PACJENT = 10


T_1 = d.date(2016,1,1)
T_2 = d.date(2017,1,1)
T_3 = d.date(2018,1,1)

Pacjenci = []
Wizyty = []
Reklamacje = []
Lekarze = []
Diagnozy = []
Leki = []
Skierowania = []
Sprzety = []
Skierowanianazabiegi = []
Zabiegi = []

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

print(c.g.generate_pesel(d.date(1945,1,1)))

def first_point_in_time():
    LICZBA_WIZYT = c.r.randint(1,10)

    for i in range(N_PACJENT):
        Pacjenci.append(c.Pacjent(T_1, T_2))
    for i in Pacjenci:
        print(i.toSQL())
        for j in range(0,c.r.randint(1,10)):
            wizyta_temp = c.Wizyta(i,T_1,T_2)
            Wizyty.append(wizyta_temp)
            print(wizyta_temp.toSQL())





first_point_in_time()
