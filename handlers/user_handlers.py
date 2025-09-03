from datetime import datetime, date, timedelta
import requests
from config_data.config import Config, load_config
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.types import CallbackQuery, Message, URLInputFile, InputMediaPhoto, ContentType,FSInputFile
from database.database import (insert_event_db, insert_reserv_db, del_event_db, select_event_id,
                               select_event_db, select_reserv_db, del_reserv_db, select_capacity_event_db,
                               select_capacity_event, select_for_admin_reserv_db, select_event_name_db,
                               edit_name_event, edit_date_event, edit_capacity_event, edit_description_event,
                               edit_place_event, edit_entry_event, edit_start_event, edit_price_event,
                               select_one_event, select_resrv_guests_and_name_event, select_one_event_id,
                               select_user_id_reserv, cancel_reserv, edit_photo_event, edit_photo_booking,
                               edit_name_booking, select_id_list, insert_id, insert_draw, select_draws,
                               select_one_draw, insert_partaker_draw, select_one_partaker_id,
                               select_partaker_draw, insert_other_event_db, select_one_other_event,
                               select_other_event_db, del_other_event_db, edit_date_other_event, edit_name_other_event,
                               edit_description_other_event, edit_time_other_event, edit_place_other_event, edit_photo_other_event,
                               edit_url_other_event, select_other_event_id, del_draw, edit_name_draw, edit_date_draw, edit_time_draw,
                               edit_photo_draw, insert_new_users, select_date_new_users)
from keyboards.other_kb import (create_menu_kb, review_kb, send_review_kb, answer_review_kb, cancel_review_kb,
                                send_review_kb_2, cancel_answer_kb, send_answer_kb, last_review_kb, newsletter_kb,
                                draw_kb, choose_event_kb, url_event_kb, choose_add_event_kb, create_pag_kb, choose_edit_event_kb,
                                create_pag_kb_url, choose_cancel_event_kb, privacy_event_kb, privacy_review_kb)
from lexicon.lexicon import LEXICON
from filters.filters import IsAdmin
from services.file_handling import now_time, check_date, check_time, event_date, check_phone, draw_datetime


router: Router = Router()


# загружаем конфиг в переменную config
config: Config = load_config()


# Cоздаем класс StatesGroup для нашей машины состояний
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    event_choosing = State()        # Состояние выбора мероприятия
    guests_choosing = State()       # Состояние выбора количества гостей
    send_number = State()           # Состояние ввода номера телефона
    privacy = State()               # Состояние согласия с обработкой персональных данных


class FSMCancelReserv(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    show_reserv_for_cancel = State()   # Cостояние выбора мероприятия для отмены бронирования
    cancel_reservation = State()       # Состояние отмены бронирования


class FSMAdmin(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    add_event = State()       # Состояние добавления мероприятия
    add_photo_event = State() # Состояние добаления афиши мероприятия
    add_other_event = State()       # Состояние добавления мероприятия со сторонней площадки
    add_photo_other_event = State() # Состояние добаления афиши мероприятия со сторонней площадки
    choose_cancel_event = State()       # Состояние выбора мероприятия
    cancel_event = State()       # Состояние отмены мероприятия
    cancel_other_event = State()       # Состояние отмены мероприятия со ссылкой
    show_reserv = State()     # Состояние просмотра брони на мероприятие
    edit_event = State()       # Состояние редактирования мероприятия


class FSMEditEvent(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    choose_event = State()       # Состояние выбора мероприятия
    choose_other_event = State()       # Состояние выбора мероприятия
    choose_change = State()      # Состояние выбора изменения
    choose_other_change = State()      # Состояние выбора изменения
    edit_name = State()          # Состояние изменения названия
    edit_other_name = State()          # Состояние изменения названия
    edit_date = State()          # Состояние изменения даты
    edit_other_date = State()          # Состояние изменения даты
    edit_capacity = State()      # Состояние изменения вместимости
    edit_description = State()   # Состояние изменения описания
    edit_other_description = State()   # Состояние изменения описания
    edit_place = State()         # Состояние изменения адреса
    edit_other_place = State()         # Состояние изменения адреса
    edit_entry = State()         # Состояние изменения сбора гостей
    edit_start = State()         # Состояние изменения начала
    edit_price = State()         # Состояние изменения стоимости
    edit_photo = State()         # Состояние изменения афиши
    edit_other_photo = State()         # Состояние изменения афиши
    edit_time = State()         # Состояние изменения времени начала
    edit_url = State()         # Состояние изменения ссылки


class FSMNewsletter(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    choose_nl = State()       # Состояние выбора варианты рассылки
    choose_event = State()       # Состояние выбора мероприятия
    choose_text = State()        # Состояние выбора текста рассылки
    create_new_text = State()    # Состояние создания нового текста рассылки
    send_newsletter = State()    # Состояние отправки рассылки
    create_text = State()    # Состояние создания текста рассылки
    add_photo = State() # Состояние добавления фото рассылки
    confirmation_nl = State() # Состояние подтверждения рассылки


class FSMDraw(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    draw_choosing = State()        # Состояние выбора розыгрыша
    add_draw = State()        # Состояние добавления розыгрыша
    add_photo_draw = State()        # Состояние добавления афиши розыгрыша
    cancel_draw = State()       # Состояние отмены розыгрыша
    choose_edit_draw = State()       # Состояние выбора розыгрыша
    choose_change = State()      # Состояние выбора изменения
    edit_name = State()          # Состояние изменения названия
    edit_date = State()          # Состояние изменения даты
    edit_time = State()          # Состояние изменения времени
    edit_photo = State()         # Состояние изменения афиши


# этот хэндлер будет срабатывать на команду "/start" -
# и отправлять ему стартовое меню
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_cammand(message: Message, bot: Bot):
    id_list_newsletter = select_id_list()
    if str(message.from_user.id) not in id_list_newsletter:
        user_id = message.from_user.id
        full_name = message.from_user.full_name
        username = message.from_user.username
        user_date = datetime.now().strftime('%d.%m.%Y')
        insert_id(user_id)
        insert_new_users(user_id, full_name, username, user_date)
    else:
        print('Такой id уже добавлен')
    text = f"{LEXICON['/start']}"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')


# этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    if message.from_user.id in config.tg_bot.admin_ids:
        await message.answer(LEXICON['/help_admin'], parse_mode='HTML')
    else:
        await message.answer(LEXICON['/help'], parse_mode='HTML')


# этот хэндлер будет срабатывать на команду "/privacy"
# и отправлять пользователю сообщение со ссылкой на политику конфиденциальности
@router.message(Command(commands='privacy'))
async def process_help_command(message: Message):
    # document = FSInputFile('/Users/nikita/Desktop/Документы_Никита/Stepik/Kseniya_bot/privacy.pdf')
    document = FSInputFile('/home/nikita/Kseniya_bot/privacy.pdf')
    await message.answer_document(caption=f'<b>Бот для брони зрительских мест функционирует в соответствии с требованиями Федерального закона №152-ФЗ «О персональных данных» и определяет порядок обработки персональных данных, осуществляемой Индивидуальным предпринимателем Утицыной К. С.\nОзнакомиться с политикой конфиденциальности можно в закрепленном файле</b>', document=document, protect_content=True, parse_mode='HTML')
    # await message.answer(f'<b>Бот для брони зрительских мест функционирует в соответствии с требованиями Федерального закона №152-ФЗ «О персональных данных» и определяет порядок обработки персональных данных, осуществляемой Индивидуальным предпринимателем Утицыной К. С.\nОзнакомиться с политикой конфиденциальности можно <a href="https://docs.google.com/document/d/1xIzaW9Fu-OsklM4exVVSiyLBRrsto6UG/edit?usp=sharing&ouid=102837261678226727912&rtpof=true&sd=true">здесь</a></b>', disable_web_page_preview=True, parse_mode='HTML')


# этот хэндлер будет срабатывать на callback "help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.callback_query(Text(text='help'))
async def process_help_command(callback: CallbackQuery):
    if callback.from_user.id in config.tg_bot.admin_ids:
        await callback.message.answer(LEXICON['/help_admin'], parse_mode='HTML')
    else:
        await callback.message.answer(LEXICON['/help'], parse_mode='HTML')


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text=f'Чтобы открыть меню введите команду \n/start')


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии выбора мероприятия и выбора количества гостей
@router.message(Command(commands='cancel'), StateFilter(FSMFillForm))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Бронирование мест отменено.')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# этот хэндлер будет срабатывать на callback "cancel"
# в состоянии выбора мероприятия и выбора количества гостей
@router.callback_query(Text(text='cancel'), StateFilter(FSMFillForm))
async def process_cancel_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=f'Бронирование мест отменено.')
    await callback.message.delete()
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()

# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии добавления мероприятия
@router.message(Command(commands='cancel'), StateFilter(FSMAdmin.add_event, FSMAdmin.add_photo_event,
FSMAdmin.add_other_event, FSMAdmin.add_photo_other_event))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Добавление мероприятия отменено.')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии удаления мероприятия
@router.message(Command(commands='cancel'), StateFilter(FSMAdmin.cancel_event, FSMAdmin.cancel_other_event))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Удаление мероприятия отменено.')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии отмены бронирования
@router.message(Command(commands='cancel'), StateFilter(FSMCancelReserv))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Отмена бронирования прервана.')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии отмены бронирования
@router.message(Command(commands='cancel'), StateFilter(FSMAdmin.show_reserv))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Просмотр броней прерван')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии редактирования мероприятия
@router.message(Command(commands='cancel'), StateFilter(FSMEditEvent))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Редактирование мероприятия прервано')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии отправки рассылки
@router.message(Command(commands='cancel'), StateFilter(FSMNewsletter))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Рассылка прервана')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии выбора розыгрыша
@router.message(Command(commands='cancel'), StateFilter(FSMDraw.draw_choosing))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Выбор розыгрыша прерван')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии добывления розыгрыша
@router.message(Command(commands='cancel'), StateFilter(FSMDraw.add_draw, FSMDraw.add_photo_draw))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Добавление розыгрыша прервано')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии добывления розыгрыша
@router.message(Command(commands='cancel'), StateFilter(FSMDraw.cancel_draw))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Отмена розыгрыша прервана')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии добывления розыгрыша
@router.message(Command(commands='cancel'), StateFilter(FSMDraw.choose_edit_draw,
FSMDraw.choose_change,FSMDraw.edit_date, FSMDraw.edit_date, FSMDraw.edit_time, FSMDraw.edit_photo))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Редактирование розыгрыша прервано')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду /choose
# и переводить бота в состояние ожидания выбора мероприятия
@router.message(Command(commands='choose'), StateFilter(default_state))
async def process_choose_command(message: Message, state: FSMContext):
    id_list_newsletter = select_id_list()
    if str(message.from_user.id) not in id_list_newsletter:
        user_id = massage.from_user.id
        full_name = message.from_user.full_name
        username = message.from_user.username
        user_date = datetime.now().strftime('%d.%m.%Y')
        insert_id(user_id)
        insert_new_users(user_id, full_name, username, user_date)
    else:
        print('Такой id уже добавлен')
    id_list = []
    date_list = []
    id_list_other = []
    date_list_other = []
    id_list_all = []
    date_list_all = []
    event_db = select_event_db()
    event_db_2 = select_other_event_db()
    string = 1
    if len(event_db) != 0:
        for event in event_db:
            try:
                if now_time(f'{event["date"]} {event["start"]}') < datetime.now():
                    if event_date(event["date"]) <= date.today():
                        del_event_db(event["id"])
                        cancel_reserv(event["name"])
                    continue
                date_list.append({'id': event["id"], 'date': event["date"]})
                id_list.append(event["id"])
            except:
                print("При проверке мероприятия произошла ошибка")
    if len(event_db_2) != 0:
        for event in event_db_2:
            try:
                if now_time(f'{event["date"]} {event["time"]}') < datetime.now():
                    if event_date(event["date"]) <= date.today():
                        del_other_event_db(event["id"])
                    continue
                date_list_other.append({'id': event["id"], 'date': event["date"]})
                id_list_other.append(event["id"])
            except:
                print("При проверке мероприятия произошла ошибка")
    date_list_all = date_list + date_list_other
    date_list_all = sorted(date_list_all, key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'), reverse=False)
    for i in date_list_all:
        id_list_all.append(i['id'])
    if len(id_list) == 0 and len(id_list_other) == 0:
        await message.answer(f"Упс! Кажется, на данный момент запланированных мероприятий нет.\nСледите за анонсами и новостями в нашем канале @locostandup")
    else:
        if id_list_all[string - 1] in id_list:
            one_event = select_one_event(id_list_all[string - 1])
            pag = f'{string}/{len(id_list_all)}'
            await state.update_data(string=string)
            if one_event['capacity'] != 0:
                text = f'{one_event["description"]}\nДата и время: {one_event["date"]} в {one_event["start"]}\nСбор гостей в {one_event["entry"]}\nВход: {one_event["price"]}\nАдрес: {one_event["place"]}\n'
            else:
                text = f'!!! SOLDOUT !!!\nК сожалению, на это шоу мест больше нет, но Вы можете забронировать места или приобрести билеты на другое мероприятие. Листайте карусель.\n\nДата и время: {one_event["date"]} в {one_event["start"]}\nСбор гостей в {one_event["entry"]}\nВход: {one_event["price"]}\nАдрес: {one_event["place"]}\n'
            await message.answer_photo(
                photo=one_event['photo'],
                caption=text,
                reply_markup=create_pag_kb(pag=pag, event_id=id_list_all[string - 1]))
        else:
            one_other_event = select_one_other_event(id_list_all[string - 1])
            pag = f'{string}/{len(id_list_all)}'
            text = f'{one_other_event["description"]}\nДата и время: {one_other_event["date"]} в {one_other_event["time"]}\nАдрес: {one_other_event["place"]}'
            await state.update_data(string=string)
            await message.answer_photo(
                photo=one_other_event['photo'],
                caption=text,
                reply_markup=create_pag_kb_url(pag=pag, url=one_other_event['url']))
        # Устанавливаем состояние ожидания выбора мероприятия
        await state.set_state(FSMFillForm.event_choosing)
        await state.update_data(id_list=id_list, id_list_other=id_list_other, id_list_all=id_list_all, string=string)


# Этот хэндлер будет срабатывать на callback choose
# и переводить бота в состояние ожидания выбора мероприятия
@router.callback_query(Text(text='choose'), StateFilter(default_state))
async def process_choose_command(callback: CallbackQuery, state: FSMContext):
    id_list_newsletter = select_id_list()
    if str(callback.from_user.id) not in id_list_newsletter:
        user_id = callback.from_user.id
        full_name = callback.message.from_user.full_name
        username = callback.message.from_user.username
        user_date = datetime.now().strftime('%d.%m.%Y')
        insert_id(user_id)
        insert_new_users(user_id, full_name, username, user_date)
    else:
        print('Такой id уже добавлен')
    id_list = []
    date_list = []
    id_list_other = []
    date_list_other = []
    id_list_all = []
    date_list_all = []
    event_db = select_event_db()
    event_db_2 = select_other_event_db()
    string = 1
    if len(event_db) != 0:
        for event in event_db:
            try:
                if now_time(f'{event["date"]} {event["start"]}') < datetime.now():
                    if event_date(event["date"]) <= date.today():
                        del_event_db(event["id"])
                        cancel_reserv(event["name"])
                    continue
                date_list.append({'id': event["id"], 'date': event["date"]})
                id_list.append(event["id"])
            except:
                print("При проверке мероприятия произошла ошибка")
    if len(event_db_2) != 0:
        for event in event_db_2:
            try:
                if now_time(f'{event["date"]} {event["time"]}') < datetime.now():
                    if event_date(event["date"]) <= date.today():
                        del_other_event_db(event["id"])
                    continue
                date_list_other.append({'id': event["id"], 'date': event["date"]})
                id_list_other.append(event["id"])
            except:
                print("При проверке мероприятия произошла ошибка")
    date_list_all = date_list + date_list_other
    date_list_all = sorted(date_list_all, key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'), reverse=False)
    for i in date_list_all:
        id_list_all.append(i['id'])
    if len(id_list) == 0 and len(id_list_other) == 0:
        await message.answer(f"Упс! Кажется, на данный момент запланированных мероприятий нет.\nСледите за анонсами и новостями в нашем канале @locostandup")
    else:
        if id_list_all[string - 1] in id_list:
            one_event = select_one_event(id_list_all[string - 1])
            pag = f'{string}/{len(id_list_all)}'
            await callback.message.delete()
            await state.update_data(string=string)
            if one_event['capacity'] != 0:
                text = f'{one_event["description"]}\nДата и время: {one_event["date"]} в {one_event["start"]}\nСбор гостей в {one_event["entry"]}\nВход: {one_event["price"]}\nАдрес: {one_event["place"]}\n'
            else:
                text = f'!!! SOLDOUT !!!\nК сожалению, на это шоу мест больше нет, но Вы можете забронировать места или приобрести билеты на другое мероприятие. Листайте карусель.\n\nДата и время: {one_event["date"]} в {one_event["start"]}\nСбор гостей в {one_event["entry"]}\nВход: {one_event["price"]}\nАдрес: {one_event["place"]}\n'
            await callback.message.answer_photo(
                photo=one_event['photo'],
                caption=text,
                reply_markup=create_pag_kb(pag=pag, event_id=id_list_all[string - 1]))
        else:
            one_other_event = select_one_other_event(id_list_all[string - 1])
            pag = f'{string}/{len(id_list_all)}'
            await callback.message.delete()
            text = f'{one_other_event["description"]}\nДата и время: {one_other_event["date"]} в {one_other_event["time"]}\nАдрес: {one_other_event["place"]}'
            await state.update_data(string=string)
            await callback.message.answer_photo(
                photo=one_other_event['photo'],
                caption=text,
                reply_markup=create_pag_kb_url(pag=pag, url=one_other_event['url']))
        # Устанавливаем состояние ожидания выбора мероприятия
        await state.set_state(FSMFillForm.event_choosing)
        await state.update_data(id_list=id_list, id_list_other=id_list_other, id_list_all=id_list_all, string=string)



# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время ввыбора мероприятия
@router.callback_query(Text(text='forward'), StateFilter(FSMFillForm.event_choosing))
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    db = await state.get_data()
    id_list = db['id_list']
    id_list_other = db['id_list_other']
    id_list_all = db['id_list_all']
    string=int(db['string'])
    if string < len(id_list_all):
        string += 1
    elif string == len(id_list_all):
        string = 1
    if id_list_all[string - 1] in id_list:
        one_event = select_one_event(id_list_all[string - 1])
        pag = f'{string}/{len(id_list_all)}'
        await callback.message.delete()
        await state.update_data(string=string)
        if one_event['capacity'] != 0:
            text = f'{one_event["description"]}\nДата и время: {one_event["date"]} в {one_event["start"]}\nСбор гостей в {one_event["entry"]}\nВход: {one_event["price"]}\nАдрес: {one_event["place"]}\n'
        else:
            text = f'!!! SOLDOUT !!!\nК сожалению, на это шоу мест больше нет, но Вы можете забронировать места или приобрести билеты на другое мероприятие. Листайте карусель.\n\nДата и время: {one_event["date"]} в {one_event["start"]}\nСбор гостей в {one_event["entry"]}\nВход: {one_event["price"]}\nАдрес: {one_event["place"]}\n'
        await callback.message.answer_photo(
            photo=one_event['photo'],
            caption=text,
            reply_markup=create_pag_kb(pag=pag, event_id=id_list_all[string - 1]))
    else:
        one_other_event = select_one_other_event(id_list_all[string - 1])
        pag = f'{string}/{len(id_list_all)}'
        await callback.message.delete()
        text = f'{one_other_event["description"]}\nДата и время: {one_other_event["date"]} в {one_other_event["time"]}\nАдрес: {one_other_event["place"]}'
        await state.update_data(string=string)
        await callback.message.answer_photo(
            photo=one_other_event['photo'],
            caption=text,
            reply_markup=create_pag_kb_url(pag=pag, url=one_other_event['url']))


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время ввыбора мероприятия
@router.callback_query(Text(text='backward'), StateFilter(FSMFillForm.event_choosing))
async def process_backward_press(callback: CallbackQuery,state: FSMContext):
    db = await state.get_data()
    id_list = db['id_list']
    id_list_other = db['id_list_other']
    id_list_all = db['id_list_all']
    string=int(db['string'])
    if string > 1:
        string -= 1
    elif string == 1:
        string = int(len(id_list_all))
    if id_list_all[string - 1] in id_list:
        one_event = select_one_event(id_list_all[string - 1])
        pag = f'{string}/{len(id_list_all)}'
        await callback.message.delete()
        await state.update_data(string=string)
        if one_event['capacity'] != 0:
            text = f'{one_event["description"]}\nДата и время: {one_event["date"]} в {one_event["start"]}\nСбор гостей в {one_event["entry"]}\nВход: {one_event["price"]}\nАдрес: {one_event["place"]}\n'
        else:
            text = f'!!! SOLDOUT !!!\nК сожалению, на это шоу мест больше нет, но Вы можете забронировать места или приобрести билеты на другое мероприятие. Листайте карусель.\n\nДата и время: {one_event["date"]} в {one_event["start"]}\nСбор гостей в {one_event["entry"]}\nВход: {one_event["price"]}\nАдрес: {one_event["place"]}\n'
        await callback.message.answer_photo(
            photo=one_event['photo'],
            caption=text,
            reply_markup=create_pag_kb(pag=pag, event_id=id_list_all[string - 1]))
    else:
        one_other_event = select_one_other_event(id_list_all[string - 1])
        pag = f'{string}/{len(id_list_all)}'
        await callback.message.delete()
        text = f'{one_other_event["description"]}\nДата и время: {one_other_event["date"]} в {one_other_event["time"]}\nАдрес: {one_other_event["place"]}'
        await state.update_data(string=string)
        await callback.message.answer_photo(
            photo=one_other_event['photo'],
            caption=text,
            reply_markup=create_pag_kb_url(pag=pag, url=one_other_event['url']))

# Этот хэндлер будет срабатывать, если введен корректный номер мероприятия
@router.callback_query(Text(text=[str(i()) for i in [lambda x = x: x for x in range(1, 5000)]]), StateFilter(FSMFillForm.event_choosing))
async def process_event_choosing(callback: CallbackQuery,state: FSMContext):
    db = await state.get_data()
    id_list = db['id_list']
    if int(callback.message.reply_markup.inline_keyboard[0][0].callback_data) in id_list:
        event_db = select_one_event(int(callback.message.reply_markup.inline_keyboard[0][0].callback_data))
        if event_db['capacity'] != 0:
            await callback.message.delete()
            await callback.message.answer(text=f'Вы выбрали мероприятие: "{event_db["name"]}"\n'
                                    f'На какое количество гостей вы хотите забронировать места ?\n\n'
                                    f'Чтобы прервать процесс бронирования введите команду - /cancel')
            # Cохраняем название мероприятия в хранилище по ключу "event"
            name = event_db['name']
            date = event_db['date']
            place = event_db['place']
            entry = event_db['entry']
            start = event_db['start']
            photo = event_db['photo']
            id = int(event_db['id'])
            await state.update_data(name=name, date=date, place=place, entry=entry, start=start, id=id, photo=photo)
            # Устанавливаем состояние ожидания выбора количества гостей
            await state.set_state(FSMFillForm.guests_choosing)
        else:
            await callback.message.answer(text=f'На мероприятие: "{event_db["name"]}" все места забронированы, выберите другое мероприятие\n\n'
                                    f'Чтобы прервать процесс бронирования введите команду - /cancel')
    else:
        await callback.message.answer(text=f'Введен не верный код мероприятия, попробуйте еще раз\n\n'
                                f'Чтобы прервать процесс бронирования введите команду - /cancel')


# Этот хэндлер будет срабатывать, если во время
# выбора мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.event_choosing))
async def warning_not_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе бронирования мероприятия\n\n'
             f'<i>ВЫБЕРИТЕ МЕРОПРИЯТИЕ, КОТОРОЕ ХОТИТЕ ПОСЕТИТЬ</i>❗️\n\n'
             'Если вы хотите прервать бронирование - '
             'отправьте команду /cancel', parse_mode='HTML')


# Этот хэндлер будет срабатывать, если введено корректное число гостей
@router.message(StateFilter(FSMFillForm.guests_choosing),
            lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_guests_choosing(message: Message, state: FSMContext):
    db = await state.get_data()
    capacity = int(select_capacity_event(db['id']))
    if int(message.text) <= capacity:
        # Cохраняем количество гостей в переменную guests
        guests = int(message.text)
        await state.update_data(guests=guests)
        # Устанавливаем состояние ожидания ввода номера телефона
        await state.set_state(FSMFillForm.send_number)
        await message.answer('Введите ваш номер телефона в формате: 89999999999')
    else:
        await message.answer(f'К сожалению столько свободных мест нет,'
                             f' выберети количество мест не привышающее {capacity}\n\n'
                             'Если вы хотите прервать бронирование - '
                             'отправьте команду /cancel')



# Этот хэндлер будет срабатывать, если во время
# выбора количества гостей введено что-то некорректное
@router.message(StateFilter(FSMFillForm.guests_choosing))
async def warning_not_guests(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе бронирования мероприятия\n\n'
             f'<i>ДЛЯ ВЫБОРА КОЛИЧЕСТВА ГОСТЕЙ ВВЕДИТЕ ЦЕЛОЕ ПОЛОЖИТЕЛЬНОЕ ЧИСЛО</i>❗️\n\n'
             'Если вы хотите прервать бронирование - '
             'отправьте команду /cancel', parse_mode='HTML')

# Этот хэндлер будет срабатывать, если введен корректно номер телефона
@router.message(StateFilter(FSMFillForm.send_number))
async def process_privacy_choosing(message: Message, state: FSMContext):
    if check_phone(message.text):
        # Cохраняем количество гостей в переменную guests
        phone = int(message.text)
        await state.update_data(phone=phone)
        # document = FSInputFile('/Users/nikita/Desktop/Документы_Никита/Stepik/Kseniya_bot/privacy.pdf')
        document = FSInputFile('/home/nikita/Kseniya_bot/privacy.pdf')
        await message.answer_document(caption=f'<b>Продолжая бронирование вы даёте согласие на обработку персональных данных.\n\nОзнакомиться с политикой конфиденциальности можно в закрепленном файле</b>', document=document, protect_content=True, reply_markup=privacy_event_kb(), parse_mode='HTML')
        # await message.answer(f'<b>Продолжая бронирование вы даёте согласие на обработку персональных данных.\n\nОзнакомиться с политикой конфиденциальности можно <a href="https://disk.yandex.ru/i/k6UyeYTlUI_-7Q">здесь</a></b>', disable_web_page_preview=True, reply_markup=privacy_event_kb(), parse_mode='HTML')
        # Устанавливаем состояние ожидания согласия на обработку персональных данных
        await state.set_state(FSMFillForm.privacy)
    else:
        await message.answer(f'Номер телефена введен не верно, введите номер согласно образца:\n'
                             f'89999999999\n\n'
                             'Если вы хотите прервать бронирование - '
                             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если во время
# ввода номера телефона введено что-то некорректное
@router.message(StateFilter(FSMFillForm.send_number))
async def warning_not_guests(message: Message):
    await message.answer(f'Номер телефена введен не верно, введите номер согласно образца:\n'
                         f'89999999999\n\n'
                         'Если вы хотите прервать бронирование - '
                         'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если пользователь согласен на обработку персональных данных
@router.callback_query(Text(text='privacy_ok'), StateFilter(FSMFillForm.privacy))
async def process_privacy_choosing(callback: CallbackQuery, state: FSMContext):
    db = await state.get_data()
    capacity = int(select_capacity_event(db['id']))
    new_capacity = str(capacity - db["guests"])
    edit_capacity_event(new_capacity, db['id'])
    # Добавляем в базу данных бронирование пользователя
    insert_reserv_db(str(callback.message.from_user.id), db['name'], str(db["guests"]),
                        db['date'], db["place"], db['entry'], db['start'],
                        str(callback.message.from_user.full_name), str(callback.message.from_user.username), db["phone"], db['photo'])
    # Завершаем машину состояний
    await state.clear()
    # Отправляем в чат сообщение о бронировании
    await callback.message.answer(
        text=f'Все готово! ✨\nВы забронировали {db["guests"]} мест(а) на "{db["name"]}" {db["date"]} в {db["place"]}\n'
                f'<b>Время сбора гостей {db["entry"]}</b>\n<b>Начало {db["start"]}\n</b>'
                f'Пожалуйста, приходите ко времени сбора гостей, чтобы заказать еду и напитки,'
                f' а также насладиться классной музыкой и атмосферой перед шоу 🍷\n\n'
                f'<i>Немного правил: рассадку в зале осуществляет администратор. Количество мест за столиком не всегда эквивалентно количеству мест в вашей брони. </i>'
                f'<i>Для сохранения театральной рассадки мы подсаживаем зрителей друг к другу. Надеемся на ваше понимание.</i>\n'
                f'<b><i>Для того, чтобы наверняка сидеть вместе со своими друзьями, пожалуйста, приходите ко времени сбора гостей.</i></b>\n'
                f'<i>В случае, если вы не придёте бронирование будет аннулировано в момент начала мероприятия, а ваши места предоставлены другим зрителям.</i> ⚠️\n\n'
                f'<i>Если остались вопросы пишите: @Kafa_tsk</i>\n\n'
                f'Чтобы отменить бронь введите команду\n/cancelreservation',
                parse_mode='HTML')


# Этот хэндлер будет срабатывать, если во время
# ввода номера телефона введено что-то некорректное
@router.message(StateFilter(FSMFillForm.privacy))
async def warning_not_guests(message: Message):
    await message.answer(f'Для подтверждения бронирования нажмите на кнопку "Продолжить"'
                         'Если вы хотите прервать бронирование - '
                         'отправьте команду /cancel')


# Этот хэндлер будет срабатывать на отправку команды /showreservation
# и отправлять в чат данные о бронировании, либо сообщение об отсутствии данных
@router.message(Command(commands='showreservation'), StateFilter(default_state))
async def process_showreservation_command(message: Message, state: FSMContext):
    if message.from_user.id not in config.tg_bot.admin_ids:
    # Отправляем пользователю информацию о бронировании, если оно есть в базе данных
        reserv_list = select_reserv_db(str(message.from_user.id))
        if len(reserv_list) != 0:
            booking_list = []
            num = 1
            for booking in reserv_list:
                booking_list.append(f'{num}) "{booking["event"]}"'
                                    f' на {booking["guests"]} гостей {booking["date"]}\n'
                                    f'<b>Сбор гостей в {booking["entry"]}</b>\n<b>Начало в {booking["start"]}</b>\n\n'
                                    f'<i>Адрес: {booking["place"]}</i>')
                num += 1
            bookings = f'\n\n'.join(booking_list)
            await message.answer(text=f"<b>ЗАБРОНИРОВАННЫЕ МЕРОПРИЯТИЯ</b>\n\n{bookings}\n\nЧтобы отменить бронь введите команду\n/cancelreservation",
                                 parse_mode='HTML')
        else:
            # Если бронирований нет, отправляем сообщение об отсутствии брони
            await message.answer(
                text=f'У вас пока что нет активной брони\n\n')
    else:
        events_list = []
        id_list = []
        num = 1
        event_db = select_event_db()
        if len(event_db) != 0:
            for event in event_db:
                try:
                    events_list.append(f'{num}) "{event["name"]}"\n'
                                    f'<b>КОД МЕРОПРИЯТИЯ 👉🏻 {event["id"]}</b>')
                    id_list.append(event["id"])
                except:
                    print("При проверке мероприятия произошла ошибка")
                num += 1
            if len(events_list) == 0:
                await message.answer("Упс! На данный момент запланированных мероприятий нет.\nСледите за анонсами и новостями в нашем канале @locostandup")
            else:
                events = f'\n\n'.join(events_list)
                text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\nЧтобы выйти из процесса просмотра броней, введите команду - /cancel"
                await message.answer(text=text, parse_mode='HTML')
                # Устанавливаем состояние ожидания ввода названия мероприятия
                await state.set_state(FSMAdmin.show_reserv)
                await state.update_data(id_list=id_list)

# Этот хэндлер будет срабатывать на callback choose
# и переводить бота в состояние ожидания выбора мероприятия
@router.callback_query(Text(text='choose'), StateFilter(default_state))
async def process_choose_command(callback: CallbackQuery, state: FSMContext):
    id_list_newsletter = select_id_list()
    if str(callback.from_user.id) not in id_list_newsletter:
        user_id = callback.from_user.id
        insert_id(user_id)
    else:
        print('Такой id уже добавлен')
    events_list = []
    id_list = []
    num = 1
    event_db = select_event_db()
    if len(event_db) != 0:
        for event in event_db:
            try:
                if event['capacity'] == 0 or now_time(f'{event["date"]} {event["start"]}') < datetime.now():
                    if event_date(event["date"]) <= date.today():
                        del_event_db(event["id"])
                        cancel_reserv(event["name"])
                    continue
                events_list.append(f'{num}) "{event["name"]}"\n{event["description"]}\n'
                                f'Дата и время: {event["date"]} в {event["start"]}\n'
                                f'Сбор гостей в {event["entry"]}\n'
                                f'Вход: {event["price"]}\n'
                                f'Адрес: {event["place"]}\n'
                                f'<b>КОД МЕРОПРИЯТИЯ 👉🏻 {event["id"]}</b>')
                id_list.append(event["id"])
            except:
                print("При проверке мероприятия произошла ошибка")
            num += 1
        if len(events_list) == 0:
            await callback.message.answer("Упс! На данный момент запланированных мероприятий нет.\nСледите за анонсами и новостями в нашем канале @locostandup")
        else:
            events = f'\n\n'.join(events_list)
            text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\nЧтобы прервать процесс бронирования введите команду - /cancel"
            await callback.message.answer(text=text, parse_mode='HTML')
            # Устанавливаем состояние ожидания выбора мероприятия
            await state.set_state(FSMFillForm.event_choosing)
            await state.update_data(id_list=id_list)


# Этот хэндлер будет срабатывать на отправку callback showreservation
# и отправлять в чат данные о бронировании, либо сообщение об отсутствии данных
@router.callback_query(Text(text='showreservation'), StateFilter(default_state))
async def process_showreservation_command(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in config.tg_bot.admin_ids:
    # Отправляем пользователю информацию о бронировании, если оно есть в базе данных
        reserv_list = select_reserv_db(str(callback.from_user.id))
        if len(reserv_list) != 0:
            booking_list = []
            num = 1
            for booking in reserv_list:
                booking_list.append(f'{num}) "{booking["event"]}"'
                                    f' на {booking["guests"]} гостей {booking["date"]}\n'
                                    f'<b>Сбор гостей в {booking["entry"]}</b>\n<b>Начало в {booking["start"]}</b>\n\n'
                                    f'<i>Адрес: {booking["place"]}</i>')
                num += 1
            bookings = f'\n\n'.join(booking_list)
            await callback.message.answer(text=f"<b>ЗАБРОНИРОВАННЫЕ МЕРОПРИЯТИЯ</b>\n\n{bookings}\n\nЧтобы отменить бронь введите команду\n/cancelreservation",
                                 parse_mode='HTML')
        else:
            # Если бронирования в базе нет - предлагаем выбрать
            await callback.message.answer(
                text=f'У вас пока что нет активной брони\n')
    else:
        events_list = []
        id_list = []
        num = 1
        event_db = select_event_db()
        if len(event_db) != 0:
            for event in event_db:
                try:
                    events_list.append(f'{num}) "{event["name"]}"\n'
                                    f'<b>КОД МЕРОПРИЯТИЯ 👉🏻 {event["id"]}</b>')
                    id_list.append(event["id"])
                except:
                    print("При проверке мероприятия произошла ошибка")
                num += 1
            if len(events_list) == 0:
                await callback.message.answer("Упс! На данный момент запланированных мероприятий нет.\nСледите за анонсами и новостями в нашем канале @locostandup")
            else:
                events = f'\n\n'.join(events_list)
                text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\nЧтобы выйти из процесса просмотра броней, введите команду - /cancel"
                await callback.message.answer(text=text, parse_mode='HTML')
                # Устанавливаем состояние ожидания ввода названия мероприятия
                await state.set_state(FSMAdmin.show_reserv)
                await state.update_data(id_list=id_list)


# Этот хэндлер будет срабатывать, если введено корректное название мероприятия
@router.message(StateFilter(FSMAdmin.show_reserv), lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_choose_show_reserv(message: Message, state: FSMContext):
    db = await state.get_data()
    id_list = db['id_list']
    if int(message.text) in id_list:
        # Получаем список бронирований
        event = select_one_event(int(message.text))
        reserv_list = select_for_admin_reserv_db(event['name'])
        if len(reserv_list) != 0:
            capacity = select_capacity_event_db((event['name']))
            booking_list = []
            reserved_seats = 0
            num = 1
            for booking in reserv_list:
                booking_list.append(f'{num}) {booking["user_name"]} забронировал(а) '
                                    f'{booking["guests"]} мест(а) на "{booking["event"]}"\n'
                                    f'tg: @{booking["email"]}\n'
                                    f'тел. {booking["phone"]}')
                num += 1
                reserved_seats += int(booking["guests"])
            if len(reserv_list) <= 30:
                bookings = f'\n\n'.join(booking_list)
                await message.answer(text=f"{bookings}\n\nВсего забронировано мест: {reserved_seats}\nСвободно мест: {capacity}\n\nЧтобы отменить бронь введите команду\n/cancelreservation")
            elif len(reserv_list) > 30 and len(reserv_list) <= 60:
                bookings_1 = f'\n\n'.join(booking_list[:30])
                bookings_2 = f'\n\n'.join(booking_list[30:])
                print(bookings_2)
                await message.answer(text=f"{bookings_1}")
                await message.answer(text=f'{bookings_2}\n\nВсего забронировано мест: {reserved_seats}\nСвободно мест: {capacity}\n\nЧтобы отменить бронь введите команду\n/cancelreservation')
            elif len(reserv_list) > 60 and len(reserv_list) <= 90:
                bookings_1 = f'\n\n'.join(booking_list[:30])
                bookings_2 = f'\n\n'.join(booking_list[30:60])
                bookings_3 = f'\n\n'.join(booking_list[60:90])
                await message.answer(text=f"{bookings_1}")
                await message.answer(text=f"{bookings_2}")
                await message.answer(text=f'{bookings_3}\n\nВсего забронировано мест: {reserved_seats}\nСвободно мест: {capacity}\n\nЧтобы отменить бронь введите команду\n/cancelreservation')
            else:
                bookings_1 = f'\n\n'.join(booking_list[:30])
                bookings_2 = f'\n\n'.join(booking_list[30:60])
                bookings_3 = f'\n\n'.join(booking_list[60:90])
                bookings_4 = f'\n\n'.join(booking_list[90:])
                await message.answer(text=f"{bookings_1}")
                await message.answer(text=f"{bookings_2}")
                await message.answer(text=f"{bookings_3}")
                await message.answer(text=f'{bookings_4}\n\nВсего забронировано мест: {reserved_seats}\nСвободно мест: {capacity}\n\nЧтобы отменить бронь введите команду\n/cancelreservation')
            # Завершаем машину состояний
            await state.clear()
        else:
            await message.answer(f'Брони на "{event["name"]}" пока что нет.')
            # Завершаем машину состояний
            await state.clear()
    else:
        await message.answer(f'Такого мероприятия не найдено, введите корректный код мероприятия\n\n'
                             'Чтобы выйти из процесса просмотра броней, введите команду - /cancel')

# Этот хэндлер будет срабатывать, если во время
# выбора мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMAdmin.show_reserv))
async def warning_not_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в режиме просмотра бронирований\n\n'
             f'<i>ДЛЯ ВЫБОРА МЕРОПРИЯТИЯ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\n'
             'Если вы хотите прервать просмотр бронирований - '
             'отправьте команду /cancel', parse_mode='HTML')


# Этот хэндлер будет срабатывать на отправку команды /cancelreservation
# и отправлять в чат данные о бронировании и вопрос о снятии бронирования
@router.message(Command(commands='cancelreservation'), StateFilter(default_state))
async def process_cancelreservation_command(message: Message, state: FSMContext):
    if message.from_user.id not in config.tg_bot.admin_ids:
        # Отправляем пользователю информацию о бронировании, если оно есть в базе данных
        reserv_list = select_reserv_db(str(message.from_user.id))
        if len(reserv_list) != 0:
            booking_list = []
            id_list = []
            num = 1
            for booking in reserv_list:
                booking_list.append(f'{num}) "{booking["event"]}" на {booking["guests"]} гостей {booking["date"]}\n'
                                    f'<b>Сбор гостей в {booking["entry"]}</b>\n<b>Начало в {booking["start"]}</b>\n\n'
                                    f'<i>Адрес: {booking["place"]}</i>\n\n'
                                    f'<b>КОД БРОНИРОВАНИЯ 👉🏻 {booking["id"]}</b>')
                id_list.append(booking["id"])
                num += 1
            bookings = f'\n\n'.join(booking_list)
            await state.update_data(id_list=id_list)
            await message.answer(text=f'<b>ЗАБРОНИРОВАННЫЕ МЕРОПРИЯТИЯ</b>\n\n{bookings}\n\n'
                                    f'<i>ДЛЯ ОТМЕНЫ БРОНИ ВВЕДИТЕ КОД БРОНИРОВАНИЯ</i>❗️\n\n'
                                    f'Если вы хотите прервать процесс отмены брони - '
                                    f'отправьте команду /cancel',
                                parse_mode='HTML')
            # Устанавливаем состояние ожидания выбора отмены бронирования
            await state.set_state(FSMCancelReserv.cancel_reservation)
        else:
            # Если бронирования в базе нет - предлагаем перейти к выбору мероприятия
            await message.answer(
                text=f'У вас пока что нет активной брони')
    else:
        events_list = []
        id_list = []
        num = 1
        event_db = select_event_db()
        if len(event_db) != 0:
            for event in event_db:
                try:
                    events_list.append(f'{num}) "{event["name"]}"\n'
                                    f'<b>КОД МЕРОПРИЯТИЯ 👉🏻 {event["id"]}</b>')
                    id_list.append(event["id"])
                except:
                    print("При проверке мероприятия произошла ошибка")
                num += 1
            if len(events_list) == 0:
                await message.answer("Упс! На данный момент запланированных мероприятий нет.\nСледите за анонсами и новостями в нашем канале @locostandup")
            else:
                events = f'\n\n'.join(events_list)
                text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\nЧтобы выйти из процесса отмены броней, введите команду - /cancel"
                await message.answer(text=text, parse_mode='HTML')
                # Устанавливаем состояние ожидания ввода названия мероприятия
                await state.set_state(FSMCancelReserv.show_reserv_for_cancel)
                print(id_list)
                await state.update_data(id_list=id_list)
        else:
            # Если нету активных мероприятий, то оповещвем об этом администратора
            await message.answer('Активных мероприятий пока что нет')


# Этот хэндлер будет срабатывать, если введено корректное название мероприятия
@router.message(StateFilter(FSMCancelReserv.show_reserv_for_cancel), lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_show_reservation_for_cancel(message: Message, state: FSMContext):
    db = await state.get_data()
    event_id_list = db['id_list']
    print(event_id_list)
    if int(message.text) in event_id_list:
        # Получаем список бронирований
        event = select_one_event(int(message.text))
        reserv_list = select_for_admin_reserv_db(event["name"])
        if len(reserv_list) != 0:
            capacity = select_capacity_event_db(event["name"])
            booking_list = []
            id_list = []
            reserved_seats = 0
            num = 1
            for booking in reserv_list:
                booking_list.append(f'{num}) {booking["user_name"]} забронировал(а) '
                                    f'{booking["guests"]} мест(а) на "{booking["event"]}"\n'
                                    f'tg: @{booking["email"]}\n'
                                    f'тел. {booking["phone"]}\n'
                                    f'<b>КОД БРОНИРОВАНИЯ 👉🏻 {booking["id"]}</b>')
                num += 1
                reserved_seats += int(booking["guests"])
                id_list.append(booking["id"])
            bookings = f'\n\n'.join(booking_list)
            await state.update_data(id_list=id_list)
            if len(booking_list) <= 25:
                await message.answer(text=f"{bookings}\n\nВсего забронировано мест: {reserved_seats}\nСвободно мест: {capacity}\n\nЕсли вы хотите прервать процесс отмены брони - отправьте команду /cancel'", parse_mode='HTML')
            else:
                text_1 = f'\n\n'.join(booking_list[:26])
                text_2 = f'\n\n'.join(booking_list[26:])
                await message.answer(text=text_1, parse_mode='HTML')
                await message.answer(text=f"{text_2}\n\nВсего забронировано мест: {reserved_seats}\nСвободно мест: {capacity}\n\nЕсли вы хотите прервать процесс отмены брони - отправьте команду /cancel'", parse_mode='HTML')
            # Устанавливаем состояние ожидания ввода кода бронирования
            await state.set_state(FSMCancelReserv.cancel_reservation)
        else:
            await message.answer(f'Брони на "{event["name"]}" пока что нет')
            # Завершаем машину состояний
            await state.clear()
    else:
        await message.answer(f'Такого мероприятия не найдено, введите корректный код мероприятия\n\n'
                             'Если вы хотите прервать процесс отмены брони - '
                             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если во время
# выбора мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMCancelReserv.show_reserv_for_cancel))
async def warning_not_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в режиме отмены бронирований\n\n'
             f'<i>ДЛЯ ВЫБОРА МЕРОПРИЯТИЯ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\n'
             'Если вы хотите прервать отмену бронирований - '
             'отправьте команду /cancel', parse_mode='HTML')


# Этот хэндлер будет срабатывать, если введен корректный номер бронирования
@router.message(StateFilter(FSMCancelReserv.cancel_reservation),
            lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_cancel_reservation(message: Message, state: FSMContext):
    # Получаем список бронирований
    db = await state.get_data()
    id_list = db['id_list']
    # Проверям корректность введенных данных
    if int(message.text) in id_list:
        try:
            name_and_guests = select_resrv_guests_and_name_event(int(message.text))
            event_name = name_and_guests[0]
            guests = int(name_and_guests[1])
            event_id = select_one_event_id(event_name)
            # Получаем количество свободных мест на мероприятие и добавляем количество отмененных мест
            new_capacity = int(select_capacity_event_db(event_name))
            new_capacity += guests
            # Обновляем количество мест на мероприятие
            edit_capacity_event(new_capacity, event_id)
        except:
            print('Данное мероприятие уже удалено из БД')
        finally:
            # Удаляем бронирование
            del_reserv_db(str(message.from_user.id), int(message.text))
            # Завершаем машину состояний
            await state.clear()
            # Отправляем в чат сообщение об отмене бронирования
            await message.answer(
                text=f'Бронирование отменено')
    else:
        await message.answer(f'Введен не верный код бронирования, попробуйте еще раз\n\n'
                             'Если вы хотите прервать процесс отмены брони - '
                             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если во время
# отмены бронирования будет введено что-то некорректное
@router.message(StateFilter(FSMCancelReserv.cancel_reservation))
async def del_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе отмены брони\n\n'
             f'<i>ДЛЯ ОТМЕНЫ БРОНИ ВВЕДИТЕ КОД БРОНИРОВАНИЯ</i>❗️\n\n'
             'Если вы хотите прервать процесс отмены брони - '
             'отправьте команду /cancel', parse_mode='HTML')


# Этот хэндлер будет срабатывать на отправку команды /addevent
# и отправлять в чат правила добавления мероприятия
@router.message(Command(commands='addevent'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_addevent_command(message: Message, state: FSMContext):
    await message.answer(text='Какое мероприятие добавить?', reply_markup=choose_add_event_kb())


# Этот хэндлер будет срабатывать на callback bot_add_event
# и переводить бота в состояние ожидания выбора мероприятия
@router.callback_query(Text(text='bot_add_event'), StateFilter(default_state))
async def process_choose_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['add'])
    await state.set_state(FSMAdmin.add_event)


# Этот хэндлер будет срабатывать на callback other_add_event
# и переводить бота в состояние ожидания выбора мероприятия
@router.callback_query(Text(text='other_add_event'), StateFilter(default_state))
async def process_choose_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON['other_add'])
    await state.set_state(FSMAdmin.add_other_event)


# Этот хэндлер будет добавлять мероприятие
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMAdmin.add_event))
async def process_add_event(message: Message, state: FSMContext):
    add_list = [i.strip() for i in message.text.split(';')]
    if len(add_list) == 8:
        error = 0
        if '"' in add_list[0] or "'" in add_list[0]:
            await message.answer('Нахождение ковычек в название мероприятия не допустимо, исправьте название')
            error += 1
        if not check_date(add_list[1]):
            await message.answer(f'Дата введена не в верном формате, введите дату в формате:\ndd.mm.yyyy')
            error += 1
        if not add_list[2].isdigit():
            await message.answer('Количество мест должно быть положительным числом больше нуля, исправьте количество мест')
            error += 1
        if '"' in add_list[3] or "'" in add_list[3]:
            await message.answer('Нахождение ковычек в описании мероприятия не допустимо, исправьте описание')
            error += 1
        if '"' in add_list[4] or "'" in add_list[4]:
            await message.answer('Нахождение ковычек в названии места проведения и адресе не допустимо, исправьте название места проведения и адрес')
            error += 1
        if not check_time(add_list[5]):
            await message.answer(f'Время сбора гостей введено не в верном формате, введите время в формате:\nhh:mm')
            error += 1
        if not check_time(add_list[6]):
            await message.answer(f'Время начала мероприятия введено не в верном формате, введите время в формате:\nhh:mm')
            error += 1
        if '"' in add_list[7] or "'" in add_list[7]:
            await message.answer('Нахождение ковычек в условиях входа не допустимо, исправьте условия входа')
            error += 1
        if error == 0:
            await message.answer(f'Отправьте картинку c афишей в ответ на это сообщение\n'
                             f'Если вы хотите прервать процесс добавления мероприятия - '
                             'отправьте команду /cancel')
            await state.update_data(add_list=add_list)
            # Устанавливаем состояние ожидания добаления афиши
            await state.set_state(FSMAdmin.add_photo_event)
    else:
        await message.answer(f'Введенные данные о мероприятии не корректны\n'
                             f'Скорее всего вы забыли поставить ; в конце одного из разделов или поставили лишний знак ;\n'
                             f'Сравните еще раз введенные данные с шаблоном и после исправления отправьте данные о мероприятии\n\n'
                             f'Если вы хотите прервать процесс добавления мероприятия - '
                             'отправьте команду /cancel')


# Этот хэндлер будет добавлять мероприятие
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMAdmin.add_other_event))
async def process_add_event(message: Message, state: FSMContext):
    add_list = [i.strip() for i in message.text.split(';')]
    if len(add_list) == 6:
        error = 0
        if '"' in add_list[0] or "'" in add_list[0]:
            await message.answer('Нахождение ковычек в название мероприятия не допустимо, исправьте название')
            error += 1
        if '"' in add_list[1] or "'" in add_list[1]:
            await message.answer('Нахождение ковычек в описании мероприятия не допустимо, исправьте описание')
            error += 1
        if not check_date(add_list[2]):
            await message.answer(f'Дата введена не в верном формате, введите дату в формате:\ndd.mm.yyyy')
            error += 1
        if not check_time(add_list[3]):
            await message.answer(f'Время начала мероприятия введено не в верном формате, введите время в формате:\nhh:mm')
            error += 1
        if '"' in add_list[4] or "'" in add_list[4]:
            await message.answer('Нахождение ковычек в названии места проведения и адресе не допустимо, исправьте название места проведения и адрес')
            error += 1
        if '"' in add_list[5] or "'" in add_list[5]:
            await message.answer('Нахождение ковычек у ссылки не допустимо, исправьте ссылку')
            error += 1
        if error == 0:
            await message.answer(f'Отправьте картинку c афишей в ответ на это сообщение\n'
                             f'Если вы хотите прервать процесс добавления мероприятия - '
                             'отправьте команду /cancel')
            await state.update_data(add_list=add_list)
            # Устанавливаем состояние ожидания добаления афиши
            await state.set_state(FSMAdmin.add_photo_other_event)
    else:
        await message.answer(f'Введенные данные о мероприятии не корректны\n'
                             f'Скорее всего вы забыли поставить ; в конце одного из разделов или поставили лишний знак ;\n'
                             f'Сравните еще раз введенные данные с шаблоном и после исправления отправьте данные о мероприятии\n\n'
                             f'Если вы хотите прервать процесс добавления мероприятия - '
                             'отправьте команду /cancel')


# Этот хэндлер будет добавлять мероприятие
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMAdmin.add_photo_event))
async def process_add_event(message: Message, state: FSMContext, bot: Bot):
    if message.photo:
        db = await state.get_data()
        add_list = db['add_list']
        insert_event_db(add_list[0], add_list[1], add_list[2], add_list[3],
                        add_list[4], add_list[5], add_list[6], add_list[7],
                        message.photo[0].file_id)
        await message.answer('Мероприятие добавлено')
        # Отправляем рассылку на новое мероприятие
        id_list = select_id_list()
        text = f'{add_list[0]} - {add_list[1]} уже доступно для бронирования мест.\n{add_list[3]} - {add_list[7]}.\n\nДля бронирования мест введите команду - /choose'
        for id in id_list:
                try:
                    await bot.send_photo(chat_id=id,
                                        photo=message.photo[0].file_id,
                                        caption=text)
                except:
                    print(f'Произошла ошибка при отправке рассылки по id - {id}')
        await message.answer('Рассылка отправлена')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer(f'Отправленное сообщение не является картинкой, отправте картинку афиши\n'
                             f'Если вы хотите прервать процесс добавления мероприятия - '
                             'отправьте команду /cancel')


# Этот хэндлер будет добавлять мероприятие
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMAdmin.add_photo_other_event))
async def process_add_event(message: Message, state: FSMContext, bot: Bot):
    if message.photo:
        db = await state.get_data()
        add_list = db['add_list']
        insert_other_event_db(add_list[0], add_list[1], add_list[2], add_list[3],
                        add_list[4], message.photo[0].file_id, add_list[5])
        await message.answer('Мероприятие добавлено')
        # Отправляем рассылку на новое мероприятие
        id_list = select_id_list()
        text = text = f'ДОСТУПНО НОВОЕ МЕРОПРИЯТИЕ\n\n"{add_list[0]}"\n{add_list[1]}\nДата и время: {add_list[2]} в {add_list[3]}\nАдрес: {add_list[4]}\n'
        for id in id_list:
                try:
                    await bot.send_photo(chat_id=id,
                                        photo=message.photo[0].file_id,
                                        caption=text,
                                        reply_markup=url_event_kb(add_list[5]),
                                        parse_mode='HTML')
                except:
                    print(f'Произошла ошибка при отправке рассылки по id - {id}')
        # await bot.send_photo(chat_id=1799099725,
        #                     photo=message.photo[0].file_id,
        #                     caption=text,
        #                     reply_markup=url_event_kb(add_list[5]),
        #                     parse_mode='HTML')
        # await bot.send_photo(chat_id=6469407067,
        #                     photo=message.photo[0].file_id,
        #                     caption=text,
        #                     reply_markup=url_event_kb(add_list[5]),
        #                     parse_mode='HTML')
        await message.answer('Рассылка отправлена')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer(f'Отправленное сообщение не является картинкой, отправте картинку афиши\n'
                             f'Если вы хотите прервать процесс добавления мероприятия - '
                             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать на отправку команды /cancelevent
# и отправлять в чат список мероприятий
@router.message(Command(commands='cancelevent'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_choose_editevent_command(message: Message, state: FSMContext):
    await message.answer(text='Какое мероприятие вы хотите отменить?', reply_markup=choose_cancel_event_kb())


# Этот хэндлер будет срабатывать на нажатие кнопки с отменой мероприятия в боте
# и отправлять в чат список мероприятий
@router.callback_query(Text(text='bot_cancel_event'), StateFilter(default_state))
async def process_delevent_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    events_list = []
    id_list = []
    num = 1
    event_db = select_event_db()
    if len(event_db) != 0:
        for event in event_db:
            events_list.append(f'{num}) "{event["name"]}"\n'
                                f'Дата и время проведения: {event["date"]} в {event["start"]}\n'
                                f'<b>КОД МЕРОПРИЯТИЯ 👉🏻 {event["id"]}</b>')
            id_list.append(event["id"])
            num += 1
        events = f'\n\n'.join(events_list)
        text = f"{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\nЧтобы прервать процесса отмены мероприятия, введите команду - /cancel"
        await callback.message.answer(text=text, parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора мероприятия
        await state.set_state(FSMAdmin.cancel_event)
        await state.update_data(id_list=id_list)
    else:
        await callback.message.answer(text='Мероприятий пока что нет')


# Этот хэндлер будет отпралять уведомления об отмене мероприятия и удалять мероприятие
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMAdmin.cancel_event),
lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_add_event(message: Message, state: FSMContext, bot: Bot):
    db = await state.get_data()
    id_list = db['id_list']
    if int(message.text) in id_list:
        # Получаем данные о мероприятии
        event = select_one_event(int(message.text))
        # Получаем id пользователей, у которых есть бронь на это мероприятие
        user_id_list = select_user_id_reserv(event['name'])
        # Отправляем уведомления пользователям об отмене мероприятия
        if len(user_id_list) != 0:
            for id in user_id_list:
                try:
                    text = f'Дорогой зритель, вынуждены сообщить, что мероприятие "{event["name"]}" {event["date"]} отменено по техническим причинам.\nПриносим свои извинения и ждем на наших следующих мероприятиях.'
                    await bot.send_message(int(id), text=text)
                except:
                    print('Произошла ошибка при отправке сообщения')
        # Удаляем мероприятие
        del_event_db(int(message.text))
        # Отменяем брони на данное мероприятие
        cancel_reserv(event["name"])
        await message.answer('Мероприятие отменено')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer(f'Введен не верный код мероприятия, попробуйте еще раз\n'
                             f'Если вы хотите прервать процесс отмены мероприятия - '
                             f'отправьте команду /cancel')


# Этот хэндлер будет срабатывать на нажатие кнопки с отменой мероприятия со ссылкой
# и отправлять в чат список мероприятий
@router.callback_query(Text(text='other_cancel_event'), StateFilter(default_state))
async def process_delevent_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    events_list = []
    id_list = []
    num = 1
    event_db = select_other_event_db()
    if len(event_db) != 0:
        for event in event_db:
            events_list.append(f'{num}) "{event["name"]}"\n'
                                f'Дата и время проведения: {event["date"]} в {event["time"]}\n'
                                f'<b>КОД МЕРОПРИЯТИЯ 👉🏻 {event["id"]}</b>')
            id_list.append(event["id"])
            num += 1
        events = f'\n\n'.join(events_list)
        text = f"{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\nЧтобы прервать процесса отмены мероприятия, введите команду - /cancel"
        await callback.message.answer(text=text, parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора мероприятия
        await state.set_state(FSMAdmin.cancel_other_event)
        await state.update_data(id_list=id_list)
    else:
        await callback.message.answer(text='Мероприятий пока что нет')


# Этот хэндлер будет отпралять уведомления об отмене мероприятия и удалять мероприятие
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMAdmin.cancel_other_event),
lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_add_event(message: Message, state: FSMContext, bot: Bot):
    db = await state.get_data()
    id_list = db['id_list']
    if int(message.text) in id_list:
        # Удаляем мероприятие
        del_other_event_db(int(message.text))
        await message.answer('Мероприятие отменено')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer(f'Введен не верный код мероприятия, попробуйте еще раз\n'
                             f'Если вы хотите прервать процесс отмены мероприятия - '
                             f'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если во время
# удаления мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMAdmin.cancel_event, FSMAdmin.cancel_other_event))
async def del_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе удаления мероприятия\n'
             f'Для удаления мероприятия введите код мероприятия\n'
             'Если вы хотите прервать процесс удаления - '
             'отправьте команду /cancel')



# Этот хэндлер будет срабатывать на отправку команды /editevent
# и отправлять в чат список мероприятий
@router.message(Command(commands='editevent'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_choose_editevent_command(message: Message, state: FSMContext):
    await message.answer(text='Какое мероприятие вы хотите изменить?', reply_markup=choose_edit_event_kb())


# Этот хэндлер будет срабатывать на callback bot_edit_event
# и переводить бота в состояние ожидания выбора мероприятия
@router.callback_query(Text(text='bot_edit_event'), StateFilter(default_state))
async def process_choose_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    events_list = []
    event_db = select_event_db()
    num = 1
    if len(event_db) != 0:
        for event in event_db:
            events_list.append(f'{num}) Название мероприятия: {event["name"]}\n'
                               f'Дата проведения: {event["date"]}\n'
                               f'Количество не забронированных мест: {event["capacity"]}\n'
                               f'Краткое описание мероприятия: {event["description"]}\n'
                               f'Место проведения и адрес: {event["place"]}\n'
                               f'Сбор гостей: {event["entry"]}\n'
                               f'Начало: {event["start"]}\n'
                               f'Вход: {event["price"]}\n'
                               f'<b>КОД МЕРОПРИЯТИЯ 👉🏻 {event["id"]}</b>')
            num += 1
        events = f'\n\n'.join(events_list)
        text = f"{events}\n\n<i>ВВЕДИТЕ КОД МЕРОПРИЯТИЯ, В КОТОРОЕ ХОТИТЕ ВНЕСТИ ИЗМЕНЕНИЯ</i>❗️\n\nЧтобы прервать процесса изменения мероприятия, введите команду - /cancel"
        await callback.message.answer(text=text, parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора мероприятия
        await state.set_state(FSMEditEvent.choose_event)
    else:
        await callback.message.answer(text='Мероприятий пока что нет')


# Этот хэндлер будет сохранять id мероприятия и ожидать ввод раздела, в который необходимо внести изменения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.choose_event),
lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_edit_event(message: Message, state: FSMContext):
    id_list = select_event_id()
    if int(message.text) in id_list:
        # Cохраняем id мероприятия в хранилище по ключу "id"
        id = int(message.text)
        event = select_one_event(id)
        await state.update_data(id=id, name=event["name"], date=event["date"], capacity=event["capacity"],
                                description=event["description"], place=event["place"], entry=event["entry"],
                                start=event["start"], price=event["price"], photo=event["photo"])
        await message.answer(text=f'Вы выбрали мероприятие: {event["name"]}\n\n'
                                f'Отправьте номер раздела, в который хотите внести изменение:\n'
                                f'1 - Название мероприятия\n'
                                f'2 - Дата проведения\n'
                                f'3 - Количество мест\n'
                                f'4 - Краткое описание мероприятия\n'
                                f'5 - Место проведения и адрес\n'
                                f'6 - Сбор гостей\n'
                                f'7 - Начало\n'
                                f'8 - Вход\n'
                                f'9 - Афиша\n\n'
                                f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.choose_change)
    else:
        await message.answer(f'Введены не корректные данные, чтобы выбрать мероприятие, '
                             f'в которое вы хотите внести изменения, введите код мероприятия\n'
                             f'Если вы хотите прервать процесс редактирования - отправьте команду\n/cancel')


# Этот хэндлер будет срабатывать, если во время
# изменения мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMEditEvent.choose_event))
async def del_event(message: Message):
    await message.answer(f'Введены не корректные данные, чтобы выбрать мероприятие, '
                         f'в которое вы хотите внести изменения, введите код мероприятия\n'
                         f'Если вы хотите прервать процесс редактирования - отправьте команду\n/cancel')


# Этот хэндлер будет выбирать раздел, в который необходимо внести изменения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.choose_change),
lambda x: x.text.isdigit() and 1 <= int(x.text) <= 9)
async def process_edit_event(message: Message, state: FSMContext):
    event = await state.get_data()
    if int(message.text) == 1:
        await message.answer(f'Текущее название:\n{event["name"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВОЕ НАЗВАНИЕ МЕРОПРИЯТИЯ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние изменения названия
        await state.set_state(FSMEditEvent.edit_name)
    elif int(message.text) == 2:
        await message.answer(f'Текущая дата: {event["date"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВУЮ ДАТУ ПРОВЕДЕНИЯ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_date)
    elif int(message.text) == 3:
        await message.answer(f'Текущее количество свободных мест: {event["capacity"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВОЕ КОЛИЧЕСТВО СВОБОДНЫХ МЕСТ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_capacity)
    elif int(message.text) == 4:
        await message.answer(f'Текущее краткое описание:\n{event["description"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВОЕ КРАТКОЕ ОПИСАНИЕ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_description)
    elif int(message.text) == 5:
        await message.answer(f'Текущее место проведения и адрес:\n{event["place"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВОЕ МЕСТО ПРОВЕДЕНИЯ И АДРЕС</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_place)
    elif int(message.text) == 6:
        await message.answer(f'Текущее время сбора гостей: {event["entry"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВОЕ ВРЕМЯ СБОРА ГОСТЕЙ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_entry)
    elif int(message.text) == 7:
        await message.answer(f'Текущее время начала мероприятия: {event["start"]}\n\n'
                             f'<i>ВВВЕДИТЕ НОВОЕ ВРЕМЯ НАЧАЛА МЕРОПРИЯТИЯ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_start)
    elif int(message.text) == 8:
        await message.answer(f'Текущее условия входа:\n{event["price"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВЫЕ УСЛОВИЯ ВХОДА</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_price)
    elif int(message.text) == 9:
        photo=event["photo"]
        if photo == None or photo == 'None':
            await message.answer(text=f'На данный момент у мероприятия нет афишы\n\n'
                             f'<i>В ОТВЕТ НА ЭТО СООБЩЕНИЕ ОТПРАВЬТЕ КАРТИНКУ С НОВОЙ АФИШЕЙ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        else:
            await message.answer_photo(photo=event["photo"], caption=f'Выше представлена текущая афиша\n\n'
                             f'<i>В ОТВЕТ НА ЭТО СООБЩЕНИЕ ОТПРАВЬТЕ КАРТИНКУ С НОВОЙ АФИШЕЙ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_photo)
    else:
        await message.answer(f'Введите номер раздела от 1 до 9\n\n'
                             f'Если вы хотите прервать процесс редактирования - '
                             f'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если во время
# редактирования мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMEditEvent.choose_change))
async def edit_event(message: Message):
    await message.answer(f'Введены не корректные данные, чтобы выбрать раздел, '
                         f'в который вы хотите внести изменения, введите номер раздела от 1 до 9\n\n'
                         f'Если вы хотите прервать процесс редактирования - отправьте команду\n/cancel')


# Этот хэндлер будет изменять название мероприятия
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_name))
async def process_edit_name_event(message: Message, state: FSMContext):
    new_name = message.text
    if '"' in new_name or "'" in new_name:
        await message.answer(f'Нахождение ковычек в название мероприятия не допустимо, исправьте название\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        old_name = db["name"]
        edit_name_event(new_name, id)
        edit_name_booking(new_name, old_name)
        await message.answer('Название мероприятия изменено')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять дату проведения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_date))
async def process_edit_date_event(message: Message, state: FSMContext):
    new_date = message.text
    if not check_date(new_date):
        await message.answer(f'Дата введена не в верном формате, введите дату в формате:\ndd.mm.yyyy\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_date_event(new_date, id)
        await message.answer('Дата проведения изменена')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять количество свободных мест
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_capacity))
async def process_edit_capacity_event(message: Message, state: FSMContext):
    new_capacity = message.text
    if not new_capacity.isdigit():
        await message.answer(f'Количество мест должно быть положительным числом больше нуля, исправьте количество мест\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_capacity_event(new_capacity, id)
        await message.answer('Количество свободных мест изменено')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять краткое описание
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_description))
async def process_edit_description_event(message: Message, state: FSMContext):
    new_description = message.text
    if '"' in new_description or "'" in new_description:
        await message.answer(f'Нахождение ковычек в описании мероприятия не допустимо, исправьте описание\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_description_event(new_description, id)
        await message.answer('Краткое описание изменено')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять место и адрес проведения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_place))
async def process_edit_place_event(message: Message, state: FSMContext):
    new_place = message.text
    if '"' in new_place or "'" in new_place:
        await message.answer(f'Нахождение ковычек в названии места проведения и адресе не допустимо,'
                             f' исправьте название места проведения и адрес\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_place_event(new_place, id)
        await message.answer('Место и адрес проведения изменено')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять время сбора гостей
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_entry))
async def process_edit_entry_event(message: Message, state: FSMContext):
    new_entry = message.text
    if not check_time(new_entry):
        await message.answer(f'Время сбора гостей введено не в верном формате, введите время в формате:\nhh:mm\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_entry_event(new_entry, id)
        await message.answer('Время сбора гостей изменено')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять время начала мероприятия
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_start))
async def process_edit_start_event(message: Message, state: FSMContext):
    new_start = message.text
    if not check_time(new_start):
        await message.answer(f'Время начала мероприятия введено не в верном формате, введите время в формате:\nhh:mm\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_start_event(new_start, id)
        await message.answer('Время начала мероприятия изменено')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять условия входа
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_price))
async def process_edit_price_event(message: Message, state: FSMContext):
    new_price = message.text
    if '"' in new_price or "'" in new_price:
        await message.answer(f'Нахождение ковычек в условиях входа не допустимо, исправьте условия входа\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_price_event(new_price, id)
        await message.answer('Условия входа изменены')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять афишу
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_photo))
async def process_edit_photo_event(message: Message, state: FSMContext):
    if message.photo:
        db = await state.get_data()
        new_photo = message.photo[0].file_id
        event_id = db["id"]
        event_name = db["name"]
        edit_photo_event(new_photo, event_id)
        edit_photo_booking(new_photo, event_name)
        await message.answer('Афиша изменена')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer(f'Отправленное сообщение не является картинкой, отправте картинку афиши\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')









# Этот хэндлер будет срабатывать на callback bot_edit_event
# и переводить бота в состояние ожидания выбора мероприятия
@router.callback_query(Text(text='other_edit_event'), StateFilter(default_state))
async def process_choose_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    events_list = []
    event_db = select_other_event_db()
    num = 1
    if len(event_db) != 0:
        for event in event_db:
            events_list.append(f'{num}) Название мероприятия: {event["name"]}\n'
                            #    f'Краткое описание мероприятия: {event["description"]}\n'
                               f'Дата проведения: {event["date"]}\n'
                            #    f'Время проведения: {event["time"]}\n'
                            #    f'Место проведения и адрес: {event["place"]}\n'
                               f'<b>КОД МЕРОПРИЯТИЯ 👉🏻 {event["id"]}</b>')
            num += 1
        events = f'\n\n'.join(events_list)
        text = f"{events}\n\n<i>ВВЕДИТЕ КОД МЕРОПРИЯТИЯ, В КОТОРОЕ ХОТИТЕ ВНЕСТИ ИЗМЕНЕНИЯ</i>❗️\n\nЧтобы прервать процесса изменения мероприятия, введите команду - /cancel"
        await callback.message.answer(text=text, parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора мероприятия
        await state.set_state(FSMEditEvent.choose_other_event)
    else:
        await callback.message.answer(text='Мероприятий пока что нет')


# Этот хэндлер будет сохранять id мероприятия и ожидать ввод раздела, в который необходимо внести изменения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.choose_other_event),
lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_edit_other_event(message: Message, state: FSMContext):
    id_list = select_other_event_id()
    if int(message.text) in id_list:
        # Cохраняем id мероприятия в хранилище по ключу "id"
        id = int(message.text)
        event = select_one_other_event(id)
        await state.update_data(id=id, name=event["name"], description=event["description"], date=event["date"],
                                time=event["time"], place=event["place"], photo=event["photo"], url=event["url"])
        await message.answer(text=f'Вы выбрали мероприятие: {event["name"]}\n\n'
                                f'Отправьте номер раздела, в который хотите внести изменение:\n'
                                f'1 - Название мероприятия\n'
                                f'2 - Краткое описание мероприятия\n'
                                f'3 - Дата проведения\n'
                                f'4 - Время проведения\n'
                                f'5 - Место проведения и адрес\n'
                                f'6 - Афиша\n'
                                f'7 - Ссылка\n\n'
                                f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.choose_other_change)
    else:
        await message.answer(f'Введены не корректные данные, чтобы выбрать мероприятие, '
                             f'в которое вы хотите внести изменения, введите код мероприятия\n'
                             f'Если вы хотите прервать процесс редактирования - отправьте команду\n/cancel')


# Этот хэндлер будет срабатывать, если во время
# изменения мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMEditEvent.choose_other_event))
async def del_event(message: Message):
    await message.answer(f'Введены не корректные данные, чтобы выбрать мероприятие, '
                         f'в которое вы хотите внести изменения, введите код мероприятия\n'
                         f'Если вы хотите прервать процесс редактирования - отправьте команду\n/cancel')


# Этот хэндлер будет выбирать раздел, в который необходимо внести изменения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.choose_other_change),
lambda x: x.text.isdigit() and 1 <= int(x.text) <= 7)
async def process_edit_event(message: Message, state: FSMContext):
    event = await state.get_data()
    if int(message.text) == 1:
        await message.answer(f'Текущее название:\n{event["name"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВОЕ НАЗВАНИЕ МЕРОПРИЯТИЯ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние изменения названия
        await state.set_state(FSMEditEvent.edit_other_name)
    elif int(message.text) == 2:
        await message.answer(f'Текущее краткое описание:\n{event["description"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВОЕ КРАТКОЕ ОПИСАНИЕ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_other_description)
    elif int(message.text) == 3:
        await message.answer(f'Текущая дата: {event["date"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВУЮ ДАТУ ПРОВЕДЕНИЯ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        #  Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_other_date)
    elif int(message.text) == 4:
        await message.answer(f'Текущее время начала мероприятия: {event["time"]}\n\n'
                             f'<i>ВВВЕДИТЕ НОВОЕ ВРЕМЯ НАЧАЛА МЕРОПРИЯТИЯ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_time)
    elif int(message.text) == 5:
        await message.answer(f'Текущее место проведения и адрес:\n{event["place"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВОЕ МЕСТО ПРОВЕДЕНИЯ И АДРЕС</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_other_place)
    elif int(message.text) == 6:
        await message.answer_photo(photo=event["photo"], caption=f'Выше представлена текущая афиша\n\n'
                             f'<i>В ОТВЕТ НА ЭТО СООБЩЕНИЕ ОТПРАВЬТЕ КАРТИНКУ С НОВОЙ АФИШЕЙ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_other_photo)
    elif int(message.text) == 7:
        await message.answer(f'Текущее ссылка мероприятия: {event["url"]}\n\n'
                             f'<i>ВВВЕДИТЕ НОВУЮ ССЫЛКУ НА МЕРОПРИЯТИЕ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.edit_url)
    else:
        await message.answer(f'Введите номер раздела от 1 до 7\n\n'
                             f'Если вы хотите прервать процесс редактирования - '
                             f'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если во время
# редактирования мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMEditEvent.choose_other_change))
async def edit_event(message: Message):
    await message.answer(f'Введены не корректные данные, чтобы выбрать раздел, '
                         f'в который вы хотите внести изменения, введите номер раздела от 1 до 7\n\n'
                         f'Если вы хотите прервать процесс редактирования - отправьте команду\n/cancel')


# Этот хэндлер будет изменять название мероприятия
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_other_name))
async def process_edit_name_other_event(message: Message, state: FSMContext):
    new_name = message.text
    if '"' in new_name or "'" in new_name:
        await message.answer(f'Нахождение ковычек в название мероприятия не допустимо, исправьте название\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        old_name = db["name"]
        edit_name_other_event(new_name, id)
        await message.answer('Название мероприятия изменено')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять краткое описание
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_other_description))
async def process_edit_description_other_event(message: Message, state: FSMContext):
    new_description = message.text
    if '"' in new_description or "'" in new_description:
        await message.answer(f'Нахождение ковычек в описании мероприятия не допустимо, исправьте описание\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_description_other_event(new_description, id)
        await message.answer('Краткое описание изменено')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять дату проведения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_other_date))
async def process_edit_date_other_event(message: Message, state: FSMContext):
    new_date = message.text
    if not check_date(new_date):
        await message.answer(f'Дата введена не в верном формате, введите дату в формате:\ndd.mm.yyyy\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_date_other_event(new_date, id)
        await message.answer('Дата проведения изменена')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять время начала мероприятия
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_time))
async def process_edit_time_event(message: Message, state: FSMContext):
    new_start = message.text
    if not check_time(new_start):
        await message.answer(f'Время начала мероприятия введено не в верном формате, введите время в формате:\nhh:mm\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_time_other_event(new_start, id)
        await message.answer('Время начала мероприятия изменено')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять место и адрес проведения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_other_place))
async def process_edit_place_other_event(message: Message, state: FSMContext):
    new_place = message.text
    if '"' in new_place or "'" in new_place:
        await message.answer(f'Нахождение ковычек в названии места проведения и адресе не допустимо,'
                             f' исправьте название места проведения и адрес\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_place_other_event(new_place, id)
        await message.answer('Место и адрес проведения изменено')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять афишу
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_other_photo))
async def process_edit_photo_event(message: Message, state: FSMContext):
    if message.photo:
        db = await state.get_data()
        new_photo = message.photo[0].file_id
        event_id = db["id"]
        edit_photo_other_event(new_photo, event_id)
        await message.answer('Афиша изменена')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer(f'Отправленное сообщение не является картинкой, отправте картинку афиши\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')


# Этот хэндлер будет изменять ссылку на мероприятие
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.edit_url))
async def process_edit_price_event(message: Message, state: FSMContext):
    url = message.text
    if '"' in url or "'" in url:
        await message.answer(f'Нахождение ковычек в ссылке не допустимо, исправьте ссылку\n\n'
                             f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_url_other_event(url, id)
        await message.answer('Ссылка изменена')
        # Завершаем машину состояний
        await state.clear()










# Этот хэндлер будет срабатывать на отправку команды /sendnewsletter
# и отправлять в чат доступные варианты для рассылки мероприятия
@router.message(IsAdmin(config.tg_bot.admin_ids), Command(commands='sendnewsletter'), StateFilter(default_state))
async def process_sendnewsletter_command(message: Message, state: FSMContext):
    await message.answer('Как вы хотите отправить рассылку?', reply_markup=newsletter_kb())
    await state.set_state(FSMNewsletter.choose_nl)


# этот хэндлер будет срабатывать на нажатие кнопки "Отменить отправку рассылки"
# и отменять отправку отзыва и переводить пользователя в стандартное состояние
@router.callback_query(Text(text='cancel_nl'), StateFilter(FSMNewsletter.choose_nl))
async def process_cancelnl_command(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Отправка рассылки отменена', parse_mode='HTML')



# этот хэндлер будет срабатывать на нажатие кнопки "Выбрать мероприятие для рассылки"
# и отправлять в чат доступные мероприятия для рассылки
@router.callback_query(Text(text='nl_event'), StateFilter(FSMNewsletter.choose_nl))
async def process_nlevent_command(callback: CallbackQuery, state: FSMContext):
    events_list = []
    id_list = []
    num = 1
    event_db = select_event_db()
    if len(event_db) != 0:
        for event in event_db:
            try:
                events_list.append(f'{num}) "{event["name"]}"\n'
                                f'<b>КОД МЕРОПРИЯТИЯ 👉🏻 {event["id"]}</b>')
                id_list.append(event["id"])
            except:
                print("При проверке мероприятия произошла ошибка")
            num += 1
        if len(events_list) == 0:
            await callback.message.answer("К сожалению на данный момент нет запланированных мероприятий, попробуйте проверить позже.")
        else:
            events = f'\n\n'.join(events_list)
            text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\nЧтобы прервать отправку рассылки, введите команду - /cancel"
            await callback.message.answer(text=text, parse_mode='HTML')
            # Устанавливаем состояние ожидания ввода названия мероприятия
            await state.set_state(FSMNewsletter.choose_event)
            await state.update_data(id_list=id_list)


# этот хэндлер будет срабатывать на нажатие кнопки "Отправить независимую рассылку"
@router.callback_query(Text(text='nl_not_event'), StateFilter(FSMNewsletter.choose_nl))
async def process_nlevent_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите текст рассылки', parse_mode='HTML')
    # Устанавливаем состояние ввода текста
    await state.set_state(FSMNewsletter.create_text)

# Этот хэндлер будет подтверждать текст рассылки
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMNewsletter.create_text))
async def process_send_newsletter(message: Message, state: FSMContext):
    await state.update_data(text = message.text)
    db = await state.get_data()
    if 'photo' in db.keys():
        await state.set_state(FSMNewsletter.confirmation_nl)
        await message.answer_photo(photo=db["photo"], caption=db["text"])
        await message.answer(
                text=f'Выше представлен текст рассылки\n\n'
                    f'Чтобы отправить текущий текст\nвведите - 1\n'
                    f'Чтобы изменить текст введите - 2\n\n'
                    f'Чтобы изменить фото введите - 3\n\n'
                    f'Чтобы прервать отправку рассылки, введите команду - /cancel',
                    parse_mode='HTML')
    else:
        await state.set_state(FSMNewsletter.add_photo)
        await message.answer('Добавьте фото рассылки')


# Этот хэндлер будет добавлять фото рассылки
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMNewsletter.add_photo))
async def process_add_photo_nl(message: Message, state: FSMContext):
    if message.photo:
        photo = message.photo[0].file_id
        await state.update_data(photo=photo)
        await state.set_state(FSMNewsletter.confirmation_nl)
        db = await state.get_data()
        await message.answer_photo(photo=db["photo"], caption=db["text"])
        await message.answer(
                text=f'Выше представлен текст рассылки\n\n'
                    f'Чтобы отправить текущий текст\nвведите - 1\n'
                    f'Чтобы изменить текст введите - 2\n\n'
                    f'Чтобы изменить фото введите - 3\n\n'
                    f'Чтобы прервать отправку рассылки, введите команду - /cancel',
                    parse_mode='HTML')
    else:
        await message.answer(f'Отправленное сообщение не является картинкой, отправте картинку еще раз\n'
                             f'Чтобы прервать отправку рассылки, введите команду - /cancel')


# Этот хэндлер будет подтверждать текст рассылки
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMNewsletter.confirmation_nl),
lambda x: x.text.isdigit() and 1 <= int(x.text) <= 3)
async def process_send_newsletter_not_event(message: Message, state: FSMContext, bot: Bot):
    if int(message.text) == 1:
        db = await state.get_data()
        id_list = select_id_list()
        # await bot.send_photo(chat_id=1799099725,
        #                     photo=db["photo"],
        #                     caption=db["text"])
        for id in id_list:
            try:
                await bot.send_photo(chat_id=id,
                                    photo=db["photo"],
                                    caption=db["text"])
            except:
                print(f'Произошла ошибка при отправке рассылки по id - {id}')
        await state.clear()
        await message.answer(f'Рассылка выполнена')
    elif int(message.text) == 2:
        # Устанавливаем состояние ожидания ввода названия мероприятия
        await state.set_state(FSMNewsletter.create_text)
        await message.answer(f'Введите новый текст рассылки\n\n'
                             'Чтобы прервать отправку рассылки, введите команду - /cancel')
    elif int(message.text) == 3:
        # Устанавливаем состояние добавления фото
        await state.set_state(FSMNewsletter.add_photo)
        await message.answer(f'Добавьте новое фото рассылки\n\n'
                             'Чтобы прервать отправку рассылки, введите команду - /cancel')


# Этот хэндлер будет срабатывать, если во время
# подтверждения независимой рассылки введено что-то некорректное
@router.message(StateFilter(FSMNewsletter.confirmation_nl))
async def del_event(message: Message):
    await message.answer(
            text=f'Введенно не коректное число\n\nЧтобы отправить текущий текст\nвведите - 1\n'
                 f'Чтобы изменить текст введите - 2\n\n'
                 f'Чтобы изменить фото введите - 3\n\n'
                 f'Чтобы прервать отправку рассылки, введите команду - /cancel',
                 parse_mode='HTML')


# Этот хэндлер будет срабатывать, если введено корректное название мероприятия
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMNewsletter.choose_event),
lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_choose_text_newsletter(message: Message, state: FSMContext):
    db = await state.get_data()
    id_list = db['id_list']
    if int(message.text) in id_list:
        event = select_one_event(int(message.text))
        newsletter = f'Приглашаем {event["date"]} на "{event["name"]}" в {event["place"]}\n\nНовые и лучшие шутки и атмосфера веселья ждут тебя!\n\nВход: {event["price"]}\nДля бронирования мест введите команду - /choose'
        await message.answer_photo(photo=event["photo"],
                                   caption=newsletter)
        await message.answer(
            text=f'Выше представлен текущий текст рассылки\n\n'
                 f'Чтобы отправить текущий текст\nвведите - 1\n'
                 f'Чтобы изменить текст введите - 2\n\n'
                 f'Чтобы прервать отправку рассылки, введите команду - /cancel',
            parse_mode='HTML')
        await state.update_data(event=event)
        # Устанавливаем состояние ожидания ввода названия мероприятия
        await state.set_state(FSMNewsletter.choose_text)
    else:
        await message.answer(f'Введен не верный код мероприятия, попробуйте еще раз\n\n'
                             'Чтобы прервать отправку рассылки, введите команду - /cancel')


# Этот хэндлер будет срабатывать, если во время
# выбора мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMNewsletter.choose_event))
async def warning_not_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в режиме отправки рассылки\n\n'
             f'<i>ДЛЯ ВЫБОРА МЕРОПРИЯТИЯ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\n'
             'Если вы хотите прервать отправку рассылки - '
             'отправьте команду /cancel', parse_mode='HTML')


# Этот хэндлер будет корректировать текст рассылки или оставлять типовой
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMNewsletter.choose_text),
lambda x: x.text.isdigit() and 1 <= int(x.text) <= 2)
async def process_create_text_newsletter(message: Message, state: FSMContext, bot: Bot):
    if int(message.text) == 1:
        db = await state.get_data()
        event = db["event"]
        id_list_reserv = select_user_id_reserv(event["name"])
        id_list = select_id_list()
        newsletter = f'Приглашаем {event["date"]} {event["name"]} {event["place"]}\n\nНовые и лучшие шутки и атмосфера веселья ждут тебя!\n\nВход: {event["price"]}\nДля бронирования мест введите команду - /choose'
        for id in id_list:
            if id not in id_list_reserv:
                try:
                    await bot.send_photo(chat_id=id,
                                        photo=event["photo"],
                                        caption=newsletter)
                except:
                    print(f'Произошла ошибка при отправке рассылки по id - {id}')
        await state.clear()
        await message.answer(f'Рассылка выполнена')
    elif int(message.text) == 2:
        # Устанавливаем состояние ожидания ввода названия мероприятия
        await state.set_state(FSMNewsletter.create_new_text)
        await message.answer(f'Введите новый текст рассылки\n\n'
                             'Чтобы прервать отправку рассылки, введите команду - /cancel')


# Этот хэндлер будет срабатывать, если во время
# выбора текста рассылки введено что-то некорректное
@router.message(StateFilter(FSMNewsletter.choose_text))
async def del_event(message: Message):
    await message.answer(
            text=f'Введенно не коректное число\n\nЧтобы отправить текущий текст\nвведите - 1\n'
                 f'Чтобы изменить текст введите - 2\n\n'
                 f'Чтобы прервать отправку рассылки, введите команду - /cancel',
                 parse_mode='HTML')


# Этот хэндлер будет подтверждать новый текст рассылки
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMNewsletter.create_new_text))
async def process_send_newsletter(message: Message, state: FSMContext, bot: Bot):
    db = await state.get_data()
    event = db["event"]
    newsletter = message.text
    await message.answer_photo(photo=event["photo"], caption=newsletter)
    await message.answer(
            text=f'Выше представлен измененый текст рассылки\n\n'
                 f'Чтобы отправить текущий текст\nвведите - 1\n'
                 f'Чтобы изменить текст введите - 2\n\n'
                 f'Чтобы прервать отправку рассылки, введите команду - /cancel',
                 parse_mode='HTML')
    await state.update_data(text=newsletter)
    await state.set_state(FSMNewsletter.send_newsletter)


# Этот хэндлер будет отправлять новый текст рассылки
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMNewsletter.send_newsletter),
lambda x: x.text.isdigit() and 1 <= int(x.text) <= 2)
async def process_send_newsletter(message: Message, state: FSMContext, bot: Bot):
    if int(message.text) == 1:
        db = await state.get_data()
        event = db["event"]
        id_list_reserv = select_user_id_reserv(event["name"])
        id_list = select_id_list()
        newsletter = db["text"]
        for id in id_list:
            if id not in id_list_reserv:
                try:
                    await bot.send_photo(chat_id=id,
                                        photo=event["photo"],
                                        caption=newsletter)
                except:
                    print(f'Произошла ошибка при отправке рассылки по id - {id}')
        await state.clear()
        await message.answer(f'Рассылка выполнена')
    elif int(message.text) == 2:
        # Устанавливаем состояние ожидания ввода названия мероприятия
        await state.set_state(FSMNewsletter.create_new_text)
        await message.answer(f'Введите новый текст рассылки\n\n'
                             'Чтобы прервать отправку рассылки, введите команду - /cancel')


# Этот хэндлер будет срабатывать, если во время
# подтверждения нового текста рассылки введено что-то некорректное
@router.message(StateFilter(FSMNewsletter.send_newsletter))
async def del_event(message: Message):
    await message.answer(
            text=f'Введенно не коректное число\n\nЧтобы отправить текущий текст\nвведите - 1\n'
                 f'Чтобы изменить текст введите - 2\n\n'
                 f'Чтобы прервать отправку рассылки, введите команду - /cancel',
                 parse_mode='HTML')




### Функция с отзывами


class FSMReview(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    choose_review = State()                # Состояние выбора формата отзыва
    write_review = State()                 # Состояние написания отзыва
    write_name = State()                 # Состояние ввода имени
    write_phone = State()                 # Состояние ввода номера телефона
    write_answer = State()                 # Состояние ввода ответа на отзыв
    choose_edit_send_review = State()      # Состояние выбора редактирования/отправки отзыва
    choose_edit_send_answer = State()      # Состояние выбора редактирования/отправки ответа на отзыв
    privacy = State()                      # Состояние уведомления о политеке конфиденциальности
    privacy_ok = State()                   # Состояние согласия с обработкой персональных данных


# этот хэндлер будет срабатывать на нажатие кнопки "Оставить отзыв"
# и отправлять пользователю сообщение с выбором вариантов отправки отзыва
@router.callback_query(Text(text='review'), StateFilter(default_state))
async def process_review_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    # document = FSInputFile('/Users/nikita/Desktop/Документы_Никита/Stepik/Kseniya_bot/privacy.pdf')
    document = FSInputFile('/home/nikita/Kseniya_bot/privacy.pdf')
    await callback.message.answer_document(caption=f'<b>Бот для брони зрительских мест функционирует в соответствии с требованиями Федерального закона №152-ФЗ «О персональных данных» и определяет порядок обработки персональных данных, осуществляемой Индивидуальным предпринимателем Утицыной К. С.\nОзнакомиться с политикой конфиденциальности можно в закрепленном файле</b>', document=document, protect_content=True, reply_markup=privacy_review_kb(), parse_mode='HTML')
    # await callback.message.answer(f'<b>Бот для брони зрительских мест функционирует в соответствии с требованиями Федерального закона №152-ФЗ «О персональных данных» и определяет порядок обработки персональных данных, осуществляемой Индивидуальным предпринимателем Утицыной К. С.\nОзнакомиться с политикой конфиденциальности можно <a href="https://disk.yandex.ru/i/k6UyeYTlUI_-7Q">здесь</a></b>', disable_web_page_preview=True, reply_markup=privacy_review_kb(), parse_mode='HTML')
    await state.set_state(FSMReview.privacy)



# этот хэндлер будет срабатывать на нажатие кнопки "Оставить отзыв"
# и отправлять пользователю сообщение с выбором вариантов отправки отзыва
@router.callback_query(Text(text='privacy_ok'), StateFilter(FSMReview.privacy))
async def process_review_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await state.set_state(FSMReview.choose_review)
    await callback.message.answer('Как вы хотите отправить отзыв ?', reply_markup=review_kb(), parse_mode='HTML')
    id = callback.from_user.id
    await state.update_data(id=id)


# этот хэндлер будет срабатывать на нажатие кнопки "Отменить отправку отзыва"
# и отменять отправку отзыва и переводить пользователя в стандартное состояние
@router.callback_query(Text(text='cancel_review'), StateFilter(FSMReview))
async def process_cancelreview_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Отправка отзыва отменена', parse_mode='HTML')


# этот хэндлер будет срабатывать на нажатие кнопки "Отменить отправку ответа на отзыв"
# и отменять отправку отзыва и переводить пользователя в стандартное состояние
@router.callback_query(Text(text='cancel_answer'), StateFilter(FSMReview))
async def process_cancelreview_command(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Отправка ответа на отзыв отменена', parse_mode='HTML')


# этот хэндлер будет срабатывать на нажатие кнопки "Анонимно"
# отправлять пользователю сообщение  о вводе текста отзыва и
# переводить в состояние написания отзыва
@router.callback_query(Text(text='anonim'), StateFilter(FSMReview.choose_review))
async def process_anonim_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await callback.message.answer(f'Введите текст отзыва, указав мероприятие, его дату и заведение, в котором оно проходило.\nПожалуйста, опишите, как можно подробнее предмет вашего обращения.\nБлагодаря этому нам удастся как можно быстрее разрешить этот вопрос.\nНу а если вы просто хотите похвалить нас и сказать какие мы классные, то спасибо большое! :)', parse_mode='HTML', reply_markup=cancel_review_kb())
    await state.set_state(FSMReview.write_review)


# этот хэндлер будет срабатывать на нажатие кнопки "Не анонимно"
# отправлять пользователю сообщение  о вводе текста отзыва и
# переводить в состояние написания отзыва
@router.callback_query(Text(text='not_anonim'), StateFilter(FSMReview.choose_review))
async def process_not_anonim_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await callback.message.answer('<b>Продолжая действие вы даёте согласие на обработку персональных данных</b>', parse_mode='HTML', reply_markup=privacy_review_kb())
    await state.set_state(FSMReview.privacy_ok)


# этот хэндлер будет срабатывать на нажатие кнопки "Продолжить"
# отправлять пользователю сообщение  о вводе текста отзыва и
# переводить в состояние написания отзыва
@router.callback_query(Text(text='privacy_ok'), StateFilter(FSMReview.privacy_ok))
async def process_not_anonim_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await callback.message.answer('Введите ваше имя', parse_mode='HTML', reply_markup=cancel_review_kb())
    await state.set_state(FSMReview.write_name)


# этот хэндлер будет срабатывать на имени и
# отправлять сообщение об отправке номера телефона
@router.message(StateFilter(FSMReview.write_name))
async def process_write_name_command(message: Message, state: FSMContext, bot: Bot):
    name = message.text
    await state.update_data(name=name)
    db = await state.get_data()
    if 'text' in db.keys():
        await message.answer(text=f'Так будет выглядеть ваш отзыв:\n\n{db["name"]} оставил(а) отзыв\nТелефон для связи: {db["phone"]}\n\n{db["text"]}', reply_markup=send_review_kb_2(), parse_mode='HTML')
        await state.set_state(FSMReview.choose_edit_send_review)
    else:
        await message.answer(text=f'Введите ваш номер телефона в формате: 89997776644', reply_markup=cancel_review_kb(), parse_mode='HTML')
        await state.set_state(FSMReview.write_phone)


# этот хэндлер будет срабатывать на отправку имени и
# отправлять сообщение об отправке номера телефона
@router.message(StateFilter(FSMReview.write_phone))
async def process_write_name_command(message: Message, state: FSMContext, bot: Bot):
    phone = message.text
    if check_phone(phone):
        await state.update_data(phone=phone)
        db = await state.get_data()
        if 'text' in db.keys():
            await message.answer(text=f'Так будет выглядеть ваш отзыв:\n\n{db["name"]} оставил(а) отзыв\nТелефон для связи: {db["phone"]}\n\n{db["text"]}', reply_markup=send_review_kb_2(), parse_mode='HTML')
            await state.set_state(FSMReview.choose_edit_send_review)
        else:
            await message.answer(f'Введите текст отзыва, указав мероприятие, его дату и заведение, в котором оно проходило.\nПожалуйста, опишите, как можно подробнее предмет вашего обращения.\nБлагодаря этому нам удастся как можно быстрее разрешить этот вопрос.\nНу а если вы просто хотите похвалить нас и сказать какие мы классные, то спасибо большое! :)', parse_mode='HTML', reply_markup=cancel_review_kb())
            await state.set_state(FSMReview.write_review)
    else:
        await message.answer('Номер телефона введен не верно, введите номер в формате: 89997776644', parse_mode='HTML', reply_markup=cancel_review_kb())


# этот хэндлер будет срабатывать на отправку текста отзыва и
# отправлять его пользователю с двумя кнопками подтвердить отправку/изменить текст
@router.message(StateFilter(FSMReview.write_review))
async def process_anonim_command(message: Message, state: FSMContext, bot: Bot):
    text_review = message.text
    await state.update_data(text=text_review)
    db = await state.get_data()
    if 'phone' in db.keys():
        await message.answer(text=f'Так будет выглядеть ваш отзыв:\n\n{db["name"]} оставил(а) отзыв\nТелефон для связи: {db["phone"]}\n\n{db["text"]}', reply_markup=send_review_kb_2(), parse_mode='HTML')
        await state.set_state(FSMReview.choose_edit_send_review)
    else:
        await message.answer(text=f'Так будет выглядеть ваш отзыв:\n\nАнонимный пользователь оставил отзыв:\n{db["text"]}', reply_markup=send_review_kb(), parse_mode='HTML')
        await state.set_state(FSMReview.choose_edit_send_review)


# этот хэндлер будет срабатывать на нажатие кнопки "Редактировать отзыв"
# отправлять пользователю сообщение о вводе текста отзыва и
# переводить в состояние написания отзыва
@router.callback_query(Text(text='edit_review'), StateFilter(FSMReview.choose_edit_send_review))
async def process_anonim_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await callback.message.answer('Напишите новый текст отзыва', parse_mode='HTML', reply_markup=cancel_review_kb())
    await state.set_state(FSMReview.write_review)


# этот хэндлер будет срабатывать на нажатие кнопки "Редактировать имя"
# отправлять пользователю сообщение о вводе текста имени и
# переводить в состояние написания имени
@router.callback_query(Text(text='edit_name'), StateFilter(FSMReview.choose_edit_send_review))
async def process_anonim_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await callback.message.answer('Введите новое имя', parse_mode='HTML', reply_markup=cancel_review_kb())
    await state.set_state(FSMReview.write_name)


# этот хэндлер будет срабатывать на нажатие кнопки "Редактировать номер телефона"
# отправлять пользователю сообщение о вводе номера телефона и
# переводить в состояние написания номера телефона
@router.callback_query(Text(text='edit_phone'), StateFilter(FSMReview.choose_edit_send_review))
async def process_anonim_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await callback.message.answer('Введите новый номер телефона', parse_mode='HTML', reply_markup=cancel_review_kb())
    await state.set_state(FSMReview.write_phone)


# этот хэндлер будет срабатывать на нажатие кнопки "Отправить отзыв"
# отправлять пользователю сообщение о том что отзыв отправлен
@router.callback_query(Text(text='send_review'), StateFilter(FSMReview.choose_edit_send_review))
async def process_anonim_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    db = await state.get_data()
    if 'phone' in db.keys():
        await bot.send_message(chat_id=6469407067, text=f'{db["name"]} оставил(а) вам отзыв\nТелефон для связи: {db["phone"]}\nID: "{db["id"]}"\n\nТекст отзыва:\n{db["text"]}', reply_markup=answer_review_kb())
    else:
        await bot.send_message(chat_id=6469407067, text=f'Анонимный пользователь оставил вам отзыв\nID: "{db["id"]}"\n\nТекст отзыва:\n{db["text"]}', reply_markup=answer_review_kb())
    await callback.message.delete()
    await callback.message.answer(f'Спасибо за обратную связь.\nБлагодаря вам качество наших мероприятий и сервис улучшаются!', parse_mode='HTML', reply_markup=last_review_kb())
    await state.clear()



# этот хэндлер будет срабатывать на нажатие кнопки "Ответить на отзыв"
# отправлять пользователю сообщение о том что отзыв отправлен
@router.callback_query(Text(text='answer_review'), StateFilter(default_state))
async def process_anonim_command(callback: CallbackQuery, state: FSMContext):
    id = callback.message.text.split('"')[1]
    await callback.message.answer('Введите ваш ответ на отзыв', parse_mode='HTML', reply_markup=cancel_answer_kb())
    await state.set_state(FSMReview.write_answer)
    await state.update_data(id=id)


# этот хэндлер будет срабатывать на отправку текста ответа на отзывв и
# отправлять его вам с двумя кнопками подтвердить отправку/изменить текст
@router.message(StateFilter(FSMReview.write_answer))
async def process_anonim_command(message: Message, state: FSMContext, bot: Bot):
    text = message.text
    await state.update_data(text=text)
    await message.answer(text=f'Так будет выглядеть ваш ответ на отзыв:\n\n{text}', reply_markup=send_answer_kb(), parse_mode='HTML')
    await state.set_state(FSMReview.choose_edit_send_answer)


# этот хэндлер будет срабатывать на нажатие кнопки "Редактировать ответ на отзыв"
# отправлять пользователю сообщение о вводе текста отзыва и
# переводить в состояние написания отзыва
@router.callback_query(Text(text='edit_answer'), StateFilter(FSMReview.choose_edit_send_answer))
async def process_anonim_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Напишите новый текст ответа на отзыв', parse_mode='HTML', reply_markup=cancel_answer_kb())
    await state.set_state(FSMReview.write_answer)


# этот хэндлер будет срабатывать на нажатие кнопки "Отправить ответ на отзыв"
# отправлять пользователю сообщение о том что отзыв отправлен
@router.callback_query(Text(text='send_answer'), StateFilter(FSMReview.choose_edit_send_answer))
async def process_anonim_command(callback: CallbackQuery, state: FSMContext):
    db = await state.get_data()
    await bot.send_message(chat_id=db["id"], text=db["text"])
    await callback.message.delete()
    await callback.message.answer('Ответ на отзыв отправлен', parse_mode='HTML')
    await state.clear()


# этот хэндлер будет срабатывать при нажатии на кнопку "Вернуться в меню" -
# и отправлять ему стартовое меню
@router.callback_query(Text(text='menu'), StateFilter(default_state))
async def process_anonim_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    text = f"{LEXICON['/start']}"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')


# этот хэндлер будет срабатывать на команду "/users"
# и отправлять админу сообщение с количеством пользователем в бд бота
@router.message(Command(commands='users'), IsAdmin)
async def process_help_command(message: Message):
    if str(message.from_user.id) == '1799099725' or str(message.from_user.id) == '6469407067':
        id_list = select_id_list()
        id_count = len(set(id_list))
        date_list = []
        user_date = select_date_new_users()
        now_date = datetime.now().strftime('%d.%m.%Y')
        for my_date in user_date:
            last_7_days = datetime.now() - timedelta(days=7)
            my_date = datetime.strptime(my_date, '%d.%m.%Y')
            if my_date > last_7_days:
                date_list.append(my_date)
        # await message.answer(text=f'По состоянию на {date.today()} в базе данных бота - 5091 пользователь', parse_mode='HTML')
        await message.answer(text=f'По состоянию на {now_date} в базе данных бота - {id_count} пользователь, за последнюю неделю присоеденилось - {len(date_list)} пользователей', parse_mode='HTML')


# Этот хэндлер будет срабатывать на callback draw
# и переводить бота в состояние выбора розыгрыша
@router.callback_query(Text(text='draw'), StateFilter(default_state))
async def process_draw_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    id_list_newsletter = select_id_list()
    if str(callback.from_user.id) not in id_list_newsletter:
        user_id = callback.from_user.id
        insert_id(user_id)
    else:
        print('Такой id уже добавлен')
    # ФУНКЦИЯ ПРОВЕРКИ ПОДПИСКИ НА КАНАЛ
    user_channel_status = await bot.get_chat_member(chat_id='@locostandup', user_id=callback.from_user.id)
    if user_channel_status.status != 'left':
        draw_list = []
        id_list = []
        num = 1
        draw_db = select_draws()
        if len(draw_db) != 0:
            for draw in draw_db:
                try:
                    if now_time(f'{draw["date"]} {draw["time"]}') < datetime.now():
                        # if event_date(draw["date"]) <= date.today():
                        #     del_draw(draw["id"])
                        continue
                    draw_end = draw_datetime(f'{draw["date"]} {draw["time"]}')
                    draw_list.append(f'{num}) "{draw["name"]}"\n'
                                    f'Дата и время окончания регистрации: {draw["date"]} в {draw["time"]}\n'
                                    f'Розыгрыш будет проведен:\n{draw_end}\n'
                                    f'<b>КОД РОЗЫГРЫША👉🏻 {draw["id"]}</b>')
                    id_list.append(draw["id"])
                except:
                    print("При проверке розыгрыша произошла ошибка")
                num += 1
            if len(draw_list) == 0:
                await callback.message.answer(f"К сожалению на данный момент нет запланированных розыгрышей.\nСледите за анонсами и новостями в нашем канале @locostandup")
            else:
                draws = f'\n\n'.join(draw_list)
                text = f"<b>ВЫБЕРИТЕ РОЗЫГРЫШ</b>\n\n{draws}\n\n<i>ЧТОБЫ ВЫБРАТЬ РОЗЫГРЫШ ВВЕДИТЕ КОД РОЗЫГРЫША</i>❗️\n\nЧтобы прервать процесс выбора розыгрыша введите команду - /cancel"
                await callback.message.answer(text=text, parse_mode='HTML')
                # Устанавливаем состояние ожидания выбора мероприятия
                await state.set_state(FSMDraw.draw_choosing)
                await state.update_data(id_list=id_list)
        else:
            await callback.message.answer(f"К сожалению на данный момент нет запланированных розыгрышей.\nСледите за анонсами и новостями в нашем канале @locostandup")
    else:
        await callback.message.answer(text=f'Для участия в розыгрыше подпишитесь на наш канал @locostandup\n')


# Этот хэндлер будет срабатывать, если введен корректный номер мероприятия
@router.message(StateFilter(FSMDraw.draw_choosing),
            lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_draw_choosing(message: Message, state: FSMContext):
    db = await state.get_data()
    id_list = db['id_list']
    if int(message.text) in id_list:
        partaker_draw_id_list = select_partaker_draw(int(message.text))
        if str(message.from_user.id) in partaker_draw_id_list:
            await message.answer('Вы уже участвуете в этом розыгрыше')
            await state.clear()
        else:
            draw = select_one_draw(int(message.text))
            insert_partaker_draw(message.from_user.id, int(message.text), message.from_user.username, message.from_user.full_name)
            partaker_id = select_one_partaker_id(message.from_user.id, int(message.text))
            draw_end = draw_datetime(f'{draw["date"]} {draw["time"]}')
            await message.answer_photo(photo=draw["photo"], caption=f'Вы участвуете в розыгрыше:\n{draw["name"].upper()}\nВам присвоен номер 👉🏻<b>{str(partaker_id["id"]).upper()}</b>❗️❗️❗️\nОжидайте результатов:\n{draw_end}\n\nСледите за обновления в нашем канале @locostandup и сообществе вконтакте vk.com/locostandup 👌🏻', parse_mode='HTML')
            await state.clear()
    else:
        await message.answer(text=f'Введен не верный код розыгрыша, попробуйте еще раз\n\n'
                                f'Чтобы прервать процесс выбора розыгрыша введите команду - /cancel')


# Этот хэндлер будет срабатывать, если во время
# выбора мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMDraw.draw_choosing))
async def warning_not_draw(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе выбора розыгрыша\n\n'
             f'<i>ДЛЯ ВЫБОРА РОЗЫГРЫША ВВЕДИТЕ КОД РОЗЫГРЫША</i>❗️\n\n'
             'Если вы хотите прервать выбор розыгрыша - '
             'отправьте команду /cancel', parse_mode='HTML')


# Этот хэндлер будет срабатывать на отправку команды /add_draw
# и отправлять в чат правила добавления розыгрыша
@router.message(Command(commands='add_draw'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_addevent_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['add_draw'])
    await state.set_state(FSMDraw.add_draw)


# Этот хэндлер будет добавлять розыгрыш
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMDraw.add_draw))
async def process_add_draw(message: Message, state: FSMContext):
    add_list = [i.strip() for i in message.text.split(';')]
    if len(add_list) == 3:
        error = 0
        if '"' in add_list[0] or "'" in add_list[0]:
            await message.answer('Нахождение ковычек в название розыгрыша не допустимо, исправьте название')
            error += 1
        if len(add_list[0]) >= 2000:
            await message.answer(f'Название розыгрыша слишком длинное, исправьте название. Допустипое количество символом - 2000, текущее количество символов - {len(add_list[0])}')
            error += 1
        if not check_date(add_list[1]):
            await message.answer(f'Дата введена не в верном формате, введите дату в формате:\ndd.mm.yyyy')
            error += 1
        if not check_time(add_list[2]):
            await message.answer(f'Время окончания регистрации на розыгрыш введено не верно, введите время в формате:\nhh:mm')
            error += 1
        if error == 0:
            await message.answer(f'Отправьте картинку c афишей розыгрыша в ответ на это сообщение\n'
                             f'Если вы хотите прервать процесс добавления розыгрыша - '
                             'отправьте команду /cancel')
            await state.update_data(add_list=add_list)
            # Устанавливаем состояние ожидания добаления афиши
            await state.set_state(FSMDraw.add_photo_draw)
    else:
        await message.answer(f'Введенные данные о розыгрыше не корректны\n'
                             f'Скорее всего вы забыли поставить ; в конце одного из разделов или поставили лишний знак ;\n'
                             f'Сравните еще раз введенные данные с шаблоном и после исправления отправьте данные о розыгрыше\n\n'
                             f'Если вы хотите прервать добавление розыгрыша - '
                             'отправьте команду /cancel')


# Этот хэндлер будет добавлять розыгрыш
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMDraw.add_photo_draw))
async def process_add_draw(message: Message, state: FSMContext, bot: Bot):
    if message.photo:
        db = await state.get_data()
        add_list = db['add_list']
        insert_draw(add_list[0], add_list[1], add_list[2], message.photo[0].file_id)
        await message.answer('Розыгрыш добавлен')
        # Отправляем рассылку на новый розыгрыш
        id_list = select_id_list()
        text = f'Участвуй в новом розыгрыше:\n{add_list[0]}\nОкончание регистрации:\n{add_list[1]} {add_list[2]}\nРозыгрыш проходит в боте, для участия кликай кнопку ниже\nУсловия: подписка на наш канал @locostandup'
        for id in id_list:
                try:
                    await bot.send_photo(chat_id=id,
                                        photo=message.photo[0].file_id,
                                        caption=text,
                                        reply_markup=draw_kb())
                except:
                    print(f'Произошла ошибка при отправке рассылки по id - {id}')
        await message.answer('Рассылка отправлена')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer(f'Отправленное сообщение не является картинкой, отправте картинку афиши\n'
                             f'Если вы хотите прервать процесс добавления розыгрыша - '
                             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать на отправку команды /canceldraw
# и отправлять в чат список мероприятий
@router.message(Command(commands='canceldraw'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_choose_canceldraw_command(message: Message, state: FSMContext):
    draws_list = []
    id_list = []
    num = 1
    draw_db = select_draws()
    if len(draw_db) != 0:
        for draw in draw_db:
            draws_list.append(f'{num}) "{draw["name"]}"\n'
                                f'Дата и время проведения: {draw["date"]} в {draw["time"]}\n'
                                f'<b>КОД РОЗЫГРЫША 👉🏻 {draw["id"]}</b>')
            id_list.append(draw["id"])
            num += 1
        draws = f'\n\n'.join(draws_list)
        text = f"{draws}\n\n<i>ЧТОБЫ ВЫБРАТЬ РОЗЫГРЫШ ВВЕДИТЕ КОД РОЗЫГРЫША</i>❗️\n\nЧтобы прервать процесса отмены розыгрыша, введите команду - /cancel"
        await message.answer(text=text, parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора мероприятия
        await state.set_state(FSMDraw.cancel_draw)
        await state.update_data(id_list=id_list)
    else:
        await message.answer(text='Розыгрышей пока что нет')


# Этот хэндлер будет отпралять уведомления об отмене мероприятия и удалять мероприятие
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMDraw.cancel_draw),
lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_add_event(message: Message, state: FSMContext, bot: Bot):
    db = await state.get_data()
    id_list = db['id_list']
    if int(message.text) in id_list:
        # Удаляем мероприятие
        del_draw(int(message.text))
        await message.answer('Розыгрыш отменен')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer(f'Введен не верный код розыгрыша, попробуйте еще раз\n'
                             f'Если вы хотите прервать процесс отмены розыгрыша - '
                             f'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если во время
# удаления мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMDraw.cancel_draw))
async def del_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе отмены розыгрыша\n'
             f'Для отмены розыгрыша введите код розыгрыша\n'
             'Если вы хотите прервать процесс отмены розыгрыша '
             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать на отправку команды /editdraw
# и отправлять в чат список мероприятий
@router.message(Command(commands='editdraw'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_choose_editevent_command(message: Message, state: FSMContext):
    draws_list = []
    id_list = []
    num = 1
    draw_db = select_draws()
    if len(draw_db) != 0:
        for draw in draw_db:
            draws_list.append(f'{num}) "{draw["name"]}"\n'
                                f'Дата и время проведения: {draw["date"]} в {draw["time"]}\n'
                                f'<b>КОД РОЗЫГРЫША 👉🏻 {draw["id"]}</b>')
            id_list.append(draw["id"])
            num += 1
        draws = f'\n\n'.join(draws_list)
        text = f"{draws}\n\n<i>ЧТОБЫ ВЫБРАТЬ РОЗЫГРЫШ ВВЕДИТЕ КОД РОЗЫГРЫША</i>❗️\n\nЧтобы прервать процесса отмены розыгрыша, введите команду - /cancel"
        await message.answer(text=text, parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора мероприятия
        await state.set_state(FSMDraw.choose_edit_draw)
        await state.update_data(id_list=id_list)
    else:
        await message.answer(text='Розыгрышей пока что нет')


# Этот хэндлер будет сохранять id мероприятия и ожидать ввод раздела, в который необходимо внести изменения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMDraw.choose_edit_draw),
lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_edit_draw(message: Message, state: FSMContext):
    db = await state.get_data()
    id_list = db['id_list']
    if int(message.text) in id_list:
        # Cохраняем id мероприятия в хранилище по ключу "id"
        id = int(message.text)
        draw = select_one_draw(id)
        await state.update_data(id=id, name=draw["name"], date=draw["date"], time=draw["time"], photo=draw["photo"])
        await message.answer(text=f'Вы выбрали: {draw["name"]}\n\n'
                                f'Отправьте номер раздела, в который хотите внести изменение:\n'
                                f'1 - Название розыгрыша\n'
                                f'2 - Дата проведения\n'
                                f'3 - Время проведения\n'
                                f'4 - Афиша\n\n'
                                f'Чтобы прервать процесса изменения розыгрыша, введите команду - /cancel')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMDraw.choose_change)
    else:
        await message.answer(f'Введены не корректные данные, чтобы выбрать розыгрыш, '
                             f'в котором хотите внести изменения, введите код розыгрыша\n'
                             f'Если вы хотите прервать процесс редактирования - отправьте команду\n/cancel')


# Этот хэндлер будет срабатывать, если во время
# изменения мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMDraw.choose_edit_draw))
async def del_event(message: Message):
    await message.answer(f'Введены не корректные данные, чтобы выбрать розыгрыш, '
                         f'в котором хотите внести изменения, введите код розыгрыша\n'
                         f'Если вы хотите прервать процесс редактирования - отправьте команду\n/cancel')


# Этот хэндлер будет выбирать раздел, в который необходимо внести изменения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMDraw.choose_change),
lambda x: x.text.isdigit() and 1 <= int(x.text) <= 4)
async def process_edit_event(message: Message, state: FSMContext):
    draw = await state.get_data()
    if int(message.text) == 1:
        await message.answer(f'Текущее название:\n{draw["name"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВОЕ НАЗВАНИЕ РОЗЫГРЫША</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения розыгрыша, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние изменения названия
        await state.set_state(FSMDraw.edit_name)
    elif int(message.text) == 2:
        await message.answer(f'Текущая дата: {draw["date"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВУЮ ДАТУ ПРОВЕДЕНИЯ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения розыгрыша, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMDraw.edit_date)
    elif int(message.text) == 3:
        await message.answer(f'Текущее время проведения: {draw["time"]}\n\n'
                             f'<i>ВВЕДИТЕ НОВОЕ ВРЕМЯ ПРОВЕДЕНИЯ</i>❗️\n\n'
                             f'Чтобы прервать процесса изменения розыгрыша, введите команду - /cancel',
                             parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMDraw.edit_time)
    elif int(message.text) == 4:
        await message.answer_photo(photo=draw["photo"], caption=f'Выше представлена текущая афиша\n\n'
                            f'<i>В ОТВЕТ НА ЭТО СООБЩЕНИЕ ОТПРАВЬТЕ КАРТИНКУ С НОВОЙ АФИШЕЙ</i>❗️\n\n'
                            f'Чтобы прервать процесса изменения розыгрыша, введите команду - /cancel',
                            parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMDraw.edit_photo)
    else:
        await message.answer(f'Введите номер раздела от 1 до 4\n\n'
                             f'Если вы хотите прервать процесс редактирования - '
                             f'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если во время
# редактирования мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMDraw.choose_change))
async def edit_event(message: Message):
    await message.answer(f'Введены не корректные данные, чтобы выбрать раздел, '
                         f'в который вы хотите внести изменения, введите номер раздела от 1 до 4\n\n'
                         f'Если вы хотите прервать процесс редактирования - отправьте команду\n/cancel')


# Этот хэндлер будет изменять название мероприятия
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMDraw.edit_name))
async def process_edit_name_draw(message: Message, state: FSMContext):
    new_name = message.text
    if '"' in new_name or "'" in new_name:
        await message.answer(f'Нахождение ковычек в названии розыгрыша не допустимо, исправьте название\n\n'
                             f'Чтобы прервать процесса изменения розыгрыша, введите команду - /cancel')
    else:
        draw = await state.get_data()
        id = draw["id"]
        edit_name_draw(new_name, id)
        await message.answer('Название розыгрыша изменено')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять дату проведения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMDraw.edit_date))
async def process_edit_date_draw(message: Message, state: FSMContext):
    new_date = message.text
    if not check_date(new_date):
        await message.answer(f'Дата введена не в верном формате, введите дату в формате:\ndd.mm.yyyy\n\n'
                             f'Чтобы прервать процесса изменения розыгрыша, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_date_draw(new_date, id)
        await message.answer('Дата проведения изменена')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять время проведения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMDraw.edit_time))
async def process_edit_entry_event(message: Message, state: FSMContext):
    new_time = message.text
    if not check_time(new_time):
        await message.answer(f'Время проведения розыгрыша введено не в верном формате, введите время в формате:\nhh:mm\n\n'
                             f'Чтобы прервать процесса изменения розыгрыша, введите команду - /cancel')
    else:
        db = await state.get_data()
        id = db["id"]
        edit_time_draw(new_time, id)
        await message.answer('Время проведения розыгрыша изменено')
        # Завершаем машину состояний
        await state.clear()


# Этот хэндлер будет изменять афишу
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMDraw.edit_photo))
async def process_edit_photo_draw(message: Message, state: FSMContext):
    if message.photo:
        db = await state.get_data()
        new_photo = message.photo[0].file_id
        id = db["id"]
        edit_photo_draw(new_photo, id)
        await message.answer('Афиша изменена')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer(f'Отправленное сообщение не является картинкой, отправте картинку афиши\n'
                             f'Чтобы прервать процесса изменения розыгрыша, введите команду - /cancel')