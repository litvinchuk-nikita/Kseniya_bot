import sqlite3
from aiogram import Bot
from datetime import timedelta, date, datetime
import random


# def now_date():
#     date_1 = date.today() + timedelta(days=1)
#     now_date = datetime.strftime(date_1, '%d.%m.%Y')
#     return now_date

def draw_datetime(date):
    date_1 = datetime.strptime(date, '%d.%m.%Y %H:%M')
    return date_1 + timedelta(hours=1)
    # return date_1 + timedelta(seconds=15)


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
                text = f'Привет, дорогой зритель!\nВы забронировали зрительские места на "{reserv["event"]}" {reserv["date"]}\nКоличество забронированных мест - {reserv["guests"]}\nМесто проведения: {reserv["place"]}\nСбор гостей начинается в {reserv["entry"]}, начало мероприятия в {reserv["start"]}\nДо встречи 🫱🏻‍🫲🏼\n\n⚠️ если по какой-то причине вы не можете посетить наше мероприятие, пожалуйста, отмените бронь с помощью команды ниже\n/cancelreservation'
                photo = reserv['photo']
                if photo is None:
                    await bot.send_message(int(reserv['user_id']), text=text)
                else:
                    await bot.send_photo(chat_id=int(reserv['user_id']), photo=reserv['photo'], caption=text)
            except:
                print('Произошла ошибка при отправке напоминания')


def select_draws():
    try:
        draw_list = []
        # conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT name, date, time, photo, id FROM draws')
        print("Данные получены")
        draws = cur.fetchall()
        cur.close()
        for draw in draws:
            draw_list.append({'name': draw[0],
                               'date': draw[1],
                               'time': draw[2],
                               'photo': draw[3],
                               'id': draw[4]})
        return draw_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_partaker_draw_id(draw_id):
    try:
        draw_list = []
        # conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id FROM partaker_draw WHERE draw_id="%s"' % (draw_id))
        print("Данные получены")
        draws = cur.fetchall()
        cur.close()
        for draw in draws:
            draw_list.append(draw[0])
        return draw_list
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")

# print(select_partaker_draw_id(5))
# print(select_draws())

def select_partaker_draw_user_id(id):
    try:
        # conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT user_id, email, username FROM partaker_draw WHERE id="%s"' % (id))
        print("Данные получены")
        draw = cur.fetchall()
        cur.close()
        return {'user_id': draw[0][0],
                'email': draw[0][1],
                'username': draw[0][2]}
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def del_draw(draw_id):
    try:
        # conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('DELETE FROM draws WHERE id="%s";' % (draw_id))
        conn.commit()
        print("Данные удалены")
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при обновлении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")

# del_draw(6)
# print(select_draws())

def select_id_list():
    try:
        # conn = sqlite3.connect('/home/nikita/Kseniya_bot/db.sql', timeout=20)
        conn = sqlite3.connect('Kseniya_bot/db.sql', timeout=20)
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


async def send_message_interval(bot: Bot):
    draws_list = select_draws()
    for draw in draws_list:
        if draw_datetime(f'{draw["date"]} {draw["time"]}') <= datetime.now():
            all_partaker_id = select_partaker_draw_id(draw["id"])
            win = False
            while win != True:
                win_num = random.choice(all_partaker_id)
                win_user = select_partaker_draw_user_id(win_num)
                user_channel_status = await bot.get_chat_member(chat_id='@locostandup', user_id=int(win_user["user_id"]))
                if user_channel_status.status != 'left':
                    win = True
            await bot.send_photo(chat_id=win_user["user_id"], photo=draw["photo"], caption=f'ПОЗДРАВЛЯЕМ! 🎉\nВы победили в розыгрыше:\n<b>{draw["name"]}</b>\nПожалуйста, напишите @violetta_kvn_standup , чтобы получить выигрыш!', parse_mode='HTML')
            await bot.send_photo(chat_id=6469407067, photo=draw["photo"], caption=f'В <b>{draw["name"]}</b> победил пользователь {win_user["username"]}, tg: {win_user["email"]}\nСкоро он свяжется с вами', parse_mode='HTML')
            await bot.send_photo(chat_id=1328733978, photo=draw["photo"], caption=f'В <b>{draw["name"]}</b> победил пользователь {win_user["username"]}, tg: {win_user["email"]}\nСкоро он свяжется с вами', parse_mode='HTML')
            # await bot.send_photo(chat_id=1799099725, photo=draw["photo"], caption=f'Побидителем в розыгрыше <b>{draw["name"]}</b> стал {win_user["username"]} с номером <b>{win_num}</b>, tg: @{win_user["email"]}', parse_mode='HTML')
            del_draw(draw["id"])
            id_list = select_id_list()
            text = f'Итоги конкурса подведены.\nСегодня победил пользователь {win_user["username"]}, под номером {win_num}!\nПоздравляем с победой!\nВсем большое спасибо за участие.'
            for id in id_list:
                if int(id) == int(win_user["user_id"]) or int(id) == 6469407067 or int(id) == 1328733978:
                    continue
                try:
                    await bot.send_photo(chat_id=id,
                                        photo=draw["photo"],
                                        caption=text)
                except:
                    print(f'Произошла ошибка при отправке рассылки по id - {id}')
