import random as r
from datetime import timedelta
from datetime import date

PESELS = []
numery_wizyt = []

choroby = {
    "Choroba Gravesa-Basedowa" : "Kardiolog",
    "Przelom tarczycowy" : "Kardiolog",
    "Przeziebienie" : "Laryngolog",
    "Grypa" : "Laryngolog",
    "Schizofrenia" : "Psychiatra",
    "Niedocukrzenie krwi" : "Kardiolog",
    #"Bol dupy" : "Anestezjolog"
    "Wady serca" : "Kardiolog",
    "Floxal" : "Okulista",
    "Parestezje" : "Neurolog",
    "Bol gardla": "Laryngolog",
    "Promienica": "Laryngolog",
    "Katar" : "Laryngolog",
    "Ucho plywaka" : "Laryngolog",
    "Padaczka" : "Neurolog",
    "Rak zoladka" : "Onkolog",
}


def generate_pesel(data: date):

    data_str = str(data.year)[2:]+ \
          (str(data.month) if len(str(data.month))== 2 else ('0'+ str(data.month))) \
          + (str(data.day) if len(str(data.day))== 2 else '0'+ str(data.day))
    random_bit = ''
    for i in range(1,5):
        random_bit += str(r.randint(0,9))

    while data_str + random_bit in PESELS:
        random_bit = (random_bit + 1) % 10000
    return data_str+random_bit

def generate_first_name():
    return(r.choice(list(open('Imie.txt'))))[:-1]

def generate_last_name():
    return (r.choice(list(open('Nazwisko.txt'))))[:-1]

def generate_date(begin=date(2016,6,30), end=date.today()) -> date:
    return date.fromordinal(r.randint(begin.toordinal(), end.toordinal()))

def generate_reklamacja_tresc():
    return "W dniu takim i takim bylem lub bylam z wizytą u lekarza i było to dla mnie bardzo niemiłe zaskoczenie. Składam reklamacje."

def generate_skierowanie_tresc():
    return "Niezwłocznie kieruję pana/panią na dużą ilośc zabiegów."

def generate_sprzet_name():
    return (r.choice(list(open('Sprzet.txt'))))[:-1]

def generate_illness():
    return r.choice(list(choroby.keys()))

def generate_specjalizacja():
    return r.choice(list(choroby.values()))

def generate_medicine_name():
    return r.choice(list(open('LekiPoczatek.txt')))[:-1] + r.choice(list(open('LekiKoniec.txt')))[:-1]

def generate_dawkowanie():
    return str(r.randint(1,4)) + " razy dziennie przez " + str(r.randint(2,4)) + " tygodnie "

def generate_sprzet_type():
    pass

def choose_doctor(lekarze: list, choroba):
    r.shuffle(lekarze)
    for l in lekarze:
        if l.specjalizacja == choroby[choroba]:
            return l
    else:
        return r.choice(lekarze)

def choose_doctor2(lekarze: list, specj):
    r.shuffle(lekarze)
    for l in lekarze:
        if l.specjalizacja == specj:
            return l
    else:
        return r.choice(lekarze)

def choose_doctor3(lekarze:list, stanowisko:int):
    if stanowisko==3:
        return None
    if not lekarze:
        return None
    r.shuffle(lekarze)
    for l in lekarze:
        if l.stanowisko > stanowisko:
            return l
    else:
        return None

def choose_lek(leki: list, choroba):
    r.shuffle(leki)
    for l in leki:
        if l.choroba == choroba:
            return l
    else:
        return r.choice(leki)

def choose_sprzet(sprzety: list, specj):
    for s in sprzety:
        if s.typ == specj:
            return s
    return r.choice(sprzety)

def gen_state():
    return r.randint(0,2)

def get_stanowisko(x: int):
    if x == 3:
        return  "Ordynator"
    if x == 2:
        return "Opiekun"
    if x == 1:
        return "Lekarz"

def generate_hour():
    return str(r.randint(7,19)) + ":" + r.choice(["00","15","30","45"])

def gen_numerwizyty():
    return r.choice(["A","B","C","D"])+str(r.randint(11111,999999))
