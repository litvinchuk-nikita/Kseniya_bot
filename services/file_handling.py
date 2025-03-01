from datetime import datetime, timedelta
import re

def now_time(date):
    date_1 = datetime.strptime(date, '%d.%m.%Y %H:%M')
    return date_1


def event_date(date):
    date_1 = datetime.strptime(date, '%d.%m.%Y')
    return date_1.date() + timedelta(days=1)


def check_date(date):
    add_id = re.fullmatch(r'^[0-3][0-9]\.[0-1][0-9]\.[2][0][2][5-9]$', date)
    return True if add_id else False


def check_time(time):
    add_id = re.fullmatch(r'^[0-2][0-9]:[0-5][0-9]$', time)
    return True if add_id else False


def check_phone(phone):
    # add_id = re.fullmatch(r'^\+[7]\-\d{3}\-\d{3}-\d{2}\-\d{2}$', phone)
    add_id = re.fullmatch(r'^\d{11}$', phone)
    return True if add_id else False


def draw_datetime(date):
    date_1 = datetime.strptime(date, '%d.%m.%Y %H:%M')
    date_2 = date_1 + timedelta(hours=3)
    return datetime.strftime(date_2, '%d.%m.%Y %H:%M')