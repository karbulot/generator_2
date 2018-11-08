import random as r
from datetime import timedelta
from datetime import date

PESELS = []

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