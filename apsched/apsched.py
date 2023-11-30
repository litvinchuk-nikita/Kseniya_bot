import sqlite3
from aiogram import Bot
from datetime import timedelta, date, datetime


# def now_date():
#     date_1 = date.today() + timedelta(days=1)
#     now_date = datetime.strftime(date_1, '%d.%m.%Y')
#     return now_date


def now_date():
    date_1 = date.today()
    now_date = datetime.strftime(date_1, '%d.%m.%Y')
    return now_date


def select_all_reserv_db():
    try:
        conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        # conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT event, guests, date, place, entry, start, user_id, photo FROM user')
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
                               'user_id': reserv[6],
                               'photo': reserv[7]})
        return reservs_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


async def send_message_cron(bot: Bot):
    reserv_list = select_all_reserv_db()
    for reserv in reserv_list:
        if reserv['date'] == now_date():
            try:
                text = f'Привет, дорогой зритель!\nТы забронировал зрительские места на "{reserv["event"]}" {reserv["date"]}\nКоличество забронированных мест - {reserv["guests"]}\nМесто проведения: {reserv["place"]}\nСбор гостей начинается в {reserv["entry"]}, начало мероприятия в {reserv["start"]}\nДо встречи 🫱🏻‍🫲🏼\n\n⚠️ если по какой-то причине ты не можешь посетить наше мероприятие, пожалуйста, отмени бронь с помощью команды ниже\n/cancelreservation'
                photo = reserv['photo']
                if photo is None:
                    await bot.send_message(int(reserv['user_id']), text=text)
                else:
                    await bot.send_photo(chat_id=int(reserv['user_id']), photo=reserv['photo'], caption=text)
            except:
                print('Произошла ошибка при отправке напоминания')