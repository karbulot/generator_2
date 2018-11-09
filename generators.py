import random as r
from datetime import timedelta
from datetime import date

PESELS = []

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
    return "W dniu takim i takim byłem lub byłam z wizytą u lekarza i było to dla mnie barzdo niemiłe zaskoczenie. Składam reklamację."

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

def choose_lek(leki: list, choroba):
    r.shuffle(leki)
    for l in leki:
        if l.choroba == choroba:
            return l
    else:
        return r.choice(leki)