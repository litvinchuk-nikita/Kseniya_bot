import datetime

def now_time(date):
    date_1 = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M')
    return date_1