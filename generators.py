import random as r
from datetime import timedelta
from datetime import date

PESELS = []

def generate_pesel(data):

    pass

def generate_first_name():
    pass

def generate_last_name():
    pass

def generate_date(begin=date(2016,6,30), end=date.today()):
    return date.fromordinal(r.randint(begin.toordinal(), end.toordinal()))

def generate_reklamacja_tresc():
    pass