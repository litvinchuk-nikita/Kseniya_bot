import sqlite3


# инициализируем "базу данных" с мероприятиями
event_list: list[dict[str, str | int]] = []

# # Создаем "базу данных" пользователей
# user_dict: dict[int, list[dict[str, str | int | bool]]] = {}

def insert_event_db(name, date, capacity, description, place, entry, start, price):
    try:
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO event (name, date, capacity, description, place, entry, start, price)'
                    ' VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
                    % (name, date, capacity, description, place, entry, start, price))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_event_db(event_list):
    try:
        event_list.clear()
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT name, date, capacity, description, place, entry, start, price FROM event')
        print("Данные получены")
        events = cur.fetchall()
        cur.close()
        for event in events:
            event_list.append({'name': event[0],
                               'date': event[1],
                               'capacity': int(event[2]),
                               'description': event[3],
                               'place': event[4],
                               'entry': event[5],
                               'start': event[6],
                               'price': event[7]})
        return event_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_capacity_event_db(event_name):
    try:
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT capacity FROM event WHERE name="%s"' % (event_name))
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


def update_event_db(capacity, name):
    try:
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE event SET capacity="%s" WHERE name="%s";' % (str(capacity), name))
        conn.commit()
        print("Данные обновлены")
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при обновлении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def del_event_db(name_event):
    try:
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('DELETE FROM event WHERE name="%s";' % (name_event))
        conn.commit()
        print("Данные удалены")
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при обновлении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def insert_reserv_db(user_id, event, guests, date, place, entry, start):
    try:
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO user (user_id, event, guests, date, place, entry, start)'
                    ' VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")'
                    % (user_id, event, str(guests), date, place, entry, start))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def del_reserv_db(user_id, reserv_id):
    try:
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('DELETE FROM user WHERE user_id="%s" AND id="%s";' % (user_id, reserv_id))
        conn.commit()
        print("Данные удалены")
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при обновлении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_reserv_db(user_id):
    try:
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT event, guests, date, place, entry, start, id FROM user WHERE user_id="%s"' % (user_id))
        print("Данные получены")
        reservs = cur.fetchall()
        cur.close()
        reservs_list = []
        for reserv in reservs:
            reservs_list.append({'event': reserv[0],
                               'guests': reserv[1],
                               'date': reserv[2],
                               'place': reserv[3],
                               'entry': reserv[4],
                               'start': reserv[5],
                               'id': reserv[6]})
        return reservs_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")