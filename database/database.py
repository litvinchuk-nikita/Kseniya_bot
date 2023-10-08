import sqlite3


# инициализируем "базу данных" с мероприятиями
event_list: list[dict[str, str | int]] = []

def insert_event_db(name, date, capacity, description, place, entry, start, price):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
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
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT name, date, capacity, description, place, entry, start, price, id FROM event')
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
                               'price': event[7],
                               'id': event[8]})
        return event_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_event_name_db():
    try:
        name_list = []
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT name FROM event')
        print("Данные получены")
        events = cur.fetchall()
        cur.close()
        for name in events:
            name_list.append(name[0])
        return name_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_capacity_event_db(event_name):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
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
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
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


def del_event_db(name_event, event_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('DELETE FROM event WHERE name="%s" AND id="%s";' % (name_event, event_id))
        conn.commit()
        print("Данные удалены")
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при обновлении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def insert_reserv_db(user_id, event, guests, date, place, entry, start, user_name, email):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO user (user_id, event, guests, date, place, entry, start, user_name, email)'
                    ' VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
                    % (user_id, event, str(guests), date, place, entry, start, user_name, email))
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
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
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
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
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


def select_all_reserv_db():
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT event, guests, date, place, entry, start, user_id FROM user')
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
                               'user_id': reserv[6]})
        return reservs_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_for_admin_reserv_db(event_name):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT event, guests, user_name, email FROM user WHERE event="%s"' % (event_name))
        print("Данные получены")
        reservs = cur.fetchall()
        cur.close()
        reservs_list = []
        for reserv in reservs:
            reservs_list.append({'event': reserv[0],
                               'guests': reserv[1],
                               'user_name': reserv[2],
                               'email': reserv[3]})
        return reservs_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")