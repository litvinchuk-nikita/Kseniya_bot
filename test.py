# import sqlite3
# from datetime import datetime

# event_list: list[dict[str, str | int]] = []

# def create_table_db():
#     try:
#         conn = sqlite3.connect('Kseniya_bot/db.sql')
#         cur = conn.cursor()
#         print("База данных подключена к SQLite")
#         # cur.execute('CREATE TABLE event(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(150), date VARCHAR(10), capacity VARCHAR(4), '
#         #             'description VARCHAR(255), place VARCHAR(150), entry VARCHAR(10), start VARCHAR(10), price VARCHAR(100))')
#         cur.execute('CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id VARCHAR(15), event VARCHAR(150), guests VARCHAR(4), date VARCHAR(10), '
#                     'place VARCHAR(150), entry VARCHAR(10), start VARCHAR(10))')
#         conn.commit()
#         print("Таблица SQLite создана")
#         cur.close()
#     except sqlite3.Error as error:
#         print("Ошибка при подключении к sqlite", error)
#     finally:
#         if (conn):
#             conn.close()
#             print("Соединение с SQLite закрыто")

# def delete_table_db():
#     try:
#         conn = sqlite3.connect('Kseniya_bot/db.sql')
#         cur = conn.cursor()
#         print("База данных подключена к SQLite")
#         cur.execute('DROP TABLE user')
#         conn.commit()
#         print("Таблица SQLite удалена")
#         cur.close()
#     except sqlite3.Error as error:
#         print("Ошибка при подключении к sqlite", error)
#     finally:
#         if (conn):
#             conn.close()
#             print("Соединение с SQLite закрыто")


# def insert_event_db(name, date, capacity, description, place, entry, start, price):
#     try:
#         conn = sqlite3.connect('Kseniya_bot/db.sql')
#         cur = conn.cursor()
#         print("База данных подключена к SQLite")
#         cur.execute('INSERT INTO event (name, date, capacity, description, place, entry, start, price)'
#                     ' VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
#                     % (name, date, capacity, description, place, entry, start, price))
#         print("Данные в таблицу добавлены")
#         conn.commit()
#         cur.close()
#     except sqlite3.Error as error:
#         print("Ошибка при добавлении данных в sqlite", error.__class__, error)
#     finally:
#         if (conn):
#             conn.close()
#             print("Соединение с SQLite закрыто")


# def select_event_db(event_list):
#     try:
#         event_list.clear()
#         conn = sqlite3.connect('Kseniya_bot/db.sql')
#         cur = conn.cursor()
#         print("База данных подключена к SQLite")
#         cur.execute('SELECT name, date, capacity, description, place, entry, start, price FROM event')
#         print("Данные получены")
#         events = cur.fetchall()
#         cur.close()
#         for event in events:
#             event_list.append({'name': event[0],
#                                'date': event[1],
#                                'capacity': int(event[2]),
#                                'description': event[3],
#                                'place': event[4],
#                                'entry': event[5],
#                                'start': event[6],
#                                'price': event[7]})
#         return event_list
#     except sqlite3.Error as error:
#         print("Ошибка при получении данных из sqlite", error.__class__, error)
#     finally:
#         if (conn):
#             conn.close()
#             print("Соединение с SQLite закрыто")


# def select_capacity_event_db(event_name):
#     try:
#         conn = sqlite3.connect('Kseniya_bot/db.sql')
#         cur = conn.cursor()
#         print("База данных подключена к SQLite")
#         cur.execute('SELECT capacity FROM event WHERE name="%s"' % (event_name))
#         print("Данные получены")
#         capacity = cur.fetchall()
#         cur.close()
#         return capacity
#     except sqlite3.Error as error:
#         print("Ошибка при получении данных из sqlite", error.__class__, error)
#     finally:
#         if (conn):
#             conn.close()
#             print("Соединение с SQLite закрыто")


# def update_event_db(capacity, name):
#     try:
#         conn = sqlite3.connect('Kseniya_bot/db.sql')
#         cur = conn.cursor()
#         print("База данных подключена к SQLite")
#         cur.execute('UPDATE event SET capacity="%s" WHERE name="%s";' % (str(capacity), name))
#         conn.commit()
#         print("Данные обновлены")
#         cur.close()
#     except sqlite3.Error as error:
#         print("Ошибка при обновлении данных из sqlite", error.__class__, error)
#     finally:
#         if (conn):
#             conn.close()
#             print("Соединение с SQLite закрыто")


# def del_event_db(name_event):
#     try:
#         conn = sqlite3.connect('Kseniya_bot/db.sql')
#         cur = conn.cursor()
#         print("База данных подключена к SQLite")
#         cur.execute('DELETE FROM event WHERE name="%s";' % (name_event))
#         conn.commit()
#         print("Данные удалены")
#         cur.close()
#     except sqlite3.Error as error:
#         print("Ошибка при обновлении данных из sqlite", error.__class__, error)
#     finally:
#         if (conn):
#             conn.close()
#             print("Соединение с SQLite закрыто")


# def insert_reserv_db(user_id, event, guests, date, place, entry, start):
#     try:
#         conn = sqlite3.connect('Kseniya_bot/db.sql')
#         cur = conn.cursor()
#         print("База данных подключена к SQLite")
#         cur.execute('INSERT INTO user (user_id, event, guests, date, place, entry, start)'
#                     ' VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")'
#                     % (user_id, event, str(guests), date, place, entry, start))
#         print("Данные в таблицу добавлены")
#         conn.commit()
#         cur.close()
#     except sqlite3.Error as error:
#         print("Ошибка при добавлении данных в sqlite", error.__class__, error)
#     finally:
#         if (conn):
#             conn.close()
#             print("Соединение с SQLite закрыто")


# def del_event_db(user_id, event_name):
#     try:
#         conn = sqlite3.connect('Kseniya_bot/db.sql')
#         cur = conn.cursor()
#         print("База данных подключена к SQLite")
#         cur.execute('DELETE FROM user WHERE user_id="%s" AND event="%s";' % (user_id, event_name))
#         conn.commit()
#         print("Данные удалены")
#         cur.close()
#     except sqlite3.Error as error:
#         print("Ошибка при обновлении данных из sqlite", error.__class__, error)
#     finally:
#         if (conn):
#             conn.close()
#             print("Соединение с SQLite закрыто")


# def select_reserv_db(user_id):
#     try:
#         conn = sqlite3.connect('Kseniya_bot/db.sql')
#         cur = conn.cursor()
#         print("База данных подключена к SQLite")
#         cur.execute('SELECT event, guests, date, place, entry, start FROM user WHERE user_id="%s"' % (user_id))
#         print("Данные получены")
#         reservs = cur.fetchall()
#         cur.close()
#         reservs_list = []
#         for reserv in reservs:
#             reservs_list.append({'event': reserv[0],
#                                'guests': reserv[1],
#                                'date': reserv[2],
#                                'place': reserv[3],
#                                'entry': reserv[4],
#                                'start': reserv[5]})
#         return reservs_list
#     except sqlite3.Error as error:
#         print("Ошибка при получении данных из sqlite", error.__class__, error)
#     finally:
#         if (conn):
#             conn.close()
#             print("Соединение с SQLite закрыто")


# insert_reserv_db('123456', 'Мероприятие 2', 5, '10.10.2023', 'Место 1', '18:00', '19:00')
# insert_reserv_db('123456', 'Мероприятие 1', 5, '10.10.2023', 'Место 1', '18:00', '19:00')
# print(select_reserv_db("123456"))
# del_event_db("123456", "Мероприятие 2")
# print(select_reserv_db("123456"))
# print(select_event_db(event_list))

# def now_time(date):
#     now = datetime.today()
#     date_1 = datetime.strptime(date, '%d.%m.%Y %H:%M')
#     return date_1

# print(now_time())


# now = datetime.now()
# date_obj = datetime.strptime(date, '%d.%m.%Y %H:%M')
# print(now)
# print(date_obj)
# print(now > date_obj)


# event_db = [1, 1, 2, 3, 2, 1, 1, 1]
# for event in event_db:
#     i = 0
#     if event == 1:
#         event_db.pop(i)
#         print(event_db, i)
#     i += 1
# print(event_db, i)