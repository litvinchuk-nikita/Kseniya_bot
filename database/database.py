import sqlite3


def insert_event_db(name, date, capacity, description, place, entry, start, price, photo):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO event (name, date, capacity, description, place, entry, start, price, photo)'
                    ' VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
                    % (name, date, capacity, description, place, entry, start, price, photo))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_event_db():
    try:
        event_list = []
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


def select_one_event(id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
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
                'price': event[0][8],
                'photo': event[0][9]}
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_event_id():
    try:
        id_list = []
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id FROM event')
        print("Данные получены")
        events = cur.fetchall()
        cur.close()
        for id in events:
            id_list.append(id[0])
        return id_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_one_event_id(event_name):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id FROM event WHERE name="%s"' % (event_name))
        print("Данные получены")
        id = cur.fetchone()
        cur.close()
        return id[0]
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_capacity_event(event_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
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


def select_resrv_guests_and_name_event(id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
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


def del_event_db(event_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('DELETE FROM event WHERE id="%s";' % (event_id))
        conn.commit()
        print("Данные удалены")
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при обновлении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def insert_reserv_db(user_id, event, guests, date, place, entry, start, user_name, email, phone, photo):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO user (user_id, event, guests, date, place, entry, start, user_name, email, phone, photo)'
                    ' VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
                    % (user_id, event, str(guests), date, place, entry, start, user_name, email, phone, photo))
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


def cancel_reserv(event_name):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('DELETE FROM user WHERE event="%s";' % (event_name))
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


def select_for_admin_reserv_db(event_name):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT event, guests, user_name, email, phone, id FROM user WHERE event="%s"' % (event_name))
        print("Данные получены")
        reservs = cur.fetchall()
        cur.close()
        reservs_list = []
        for reserv in reservs:
            reservs_list.append({'event': reserv[0],
                               'guests': reserv[1],
                               'user_name': reserv[2],
                               'email': reserv[3],
                               'phone': reserv[4],
                               'id': reserv[5]})
        return reservs_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_user_id_reserv(event_name):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT user_id FROM user WHERE event="%s"' % (event_name))
        print("Данные получены")
        reservs = cur.fetchall()
        cur.close()
        reservs_list = []
        for reserv in reservs:
            reservs_list.append(reserv[0])
        return reservs_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def edit_name_event(new_name, event_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE event SET name = "%s" WHERE id = "%s"' % (new_name, event_id))
        print("Изменения внесены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def edit_name_booking(new_name, old_name):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE user SET event = "%s" WHERE event = "%s"' % (new_name, old_name))
        print("Изменения внесены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def edit_date_event(new_date, event_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE event SET date = "%s" WHERE id = "%s"' % (new_date, event_id))
        print("Изменения внесены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def edit_capacity_event(new_capacity, event_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE event SET capacity="%s" WHERE id="%s"' % (new_capacity, event_id))
        print("Изменения внесены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def edit_description_event(new_description, event_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE event SET description = "%s" WHERE id = "%s"' % (new_description, event_id))
        print("Изменения внесены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def edit_place_event(new_place, event_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE event SET place = "%s" WHERE id = "%s"' % (new_place, event_id))
        print("Изменения внесены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def edit_entry_event(new_entry, event_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE event SET entry = "%s" WHERE id = "%s"' % (new_entry, event_id))
        print("Изменения внесены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def edit_start_event(new_start, event_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE event SET start = "%s" WHERE id = "%s"' % (new_start, event_id))
        print("Изменения внесены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def edit_price_event(new_price, event_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE event SET price = "%s" WHERE id = "%s"' % (new_price, event_id))
        print("Изменения внесены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def edit_photo_event(new_photo, event_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE event SET photo = "%s" WHERE id = "%s"' % (new_photo, event_id))
        print("Изменения внесены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def edit_photo_booking(new_photo, event_name):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE user SET photo = "%s" WHERE event = "%s"' % (new_photo, event_name))
        print("Изменения внесены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_id_list():
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT user_id FROM id_list')
        print("Данные получены")
        ids = cur.fetchall()
        cur.close()
        id_list = []
        for id in ids:
            id_list.append(id[0])
        return id_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")

# id = select_id_list()
# id = set(id)
# print(id, len(id))


def insert_id(user_id):
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO id_list (user_id) VALUES ("%s")' % (user_id))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")