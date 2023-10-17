import re
import sqlite3
from datetime import datetime, timedelta, date

mess = '12.10.2023'
def check_date(date):
    add_id = re.fullmatch(r'^[0-3][0-9]\.[0-1][0-9]\.[2][0][2][3-9]$', date)
    return True if add_id else False


def check_time(time):
    add_id = re.fullmatch(r'^[0-2][0-9]:[0-5][0-9]$', time)
    return True if add_id else False


# print(check_date(mess))
# print('53a'.isdigit())
# print(check_time('19.30'))

def select_one_event(id):
    try:
        # conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT * FROM event WHERE id="%s"' % (id))
        print("Данные получены")
        event = cur.fetchall()
        cur.close()
        return {'id': event[0][0],
                'name': event[0][1],
                'date': event[0][2],
                'capacity': int(event[0][3]),
                'description': event[0][4],
                'place': event[0][5],
                'entry': event[0][6],
                'start': event[0][7],
                'price': event[0][8]}
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")

# print(select_one_event(2))


def select_capacity_event(event_id):
    try:
        # conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT capacity FROM event WHERE id="%s"' % (event_id))
        print("Данные получены")
        capacity = cur.fetchone()
        cur.close()
        return capacity[0]
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


# print(select_capacity_event(2))


def select_resrv_guests_and_name_event(id):
    try:
        # conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT event, guests FROM user WHERE id="%s"' % (id))
        print("Данные получены")
        event_name = cur.fetchall()
        cur.close()
        return event_name[0]
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


# print(select_resrv_guests_and_name_event(1))


def event_date(date):
    date_1 = datetime.strptime(date, '%d.%m.%Y')
    return date_1.date() + timedelta(days=1)


# print(event_date('17.10.2023'))
print(date.today())