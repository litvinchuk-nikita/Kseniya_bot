from datetime import datetime, date, timedelta
import requests
from config_data.config import Config, load_config
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.types import CallbackQuery, Message, URLInputFile, InputMediaPhoto, ContentType
from database.database import (insert_event_db, insert_reserv_db, del_event_db, select_event_id,
                               select_event_db, select_reserv_db, del_reserv_db, select_capacity_event_db,
                               select_capacity_event, select_for_admin_reserv_db, select_event_name_db,
                               edit_name_event, edit_date_event, edit_capacity_event, edit_description_event,
                               edit_place_event, edit_entry_event, edit_start_event, edit_price_event,
                               select_one_event, select_resrv_guests_and_name_event, select_one_event_id,
                               select_user_id_reserv, cancel_reserv)
from keyboards.other_kb import create_menu_kb
from lexicon.lexicon import LEXICON
from filters.filters import IsAdmin
from services.file_handling import now_time, check_date, check_time, event_date, check_phone

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
    cancel_event = State()       # Состояние отмены мероприятия
    show_reserv = State()     # Состояние просмотра брони на мероприятие
    edit_event = State()       # Состояние редактирования мероприятия


class FSMEditEvent(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    choose_event = State()       # Состояние выбора мероприятия
    choose_change = State()      # Состояние выбора изменения
    edit_name = State()          # Состояние изменения названия
    edit_date = State()          # Состояние изменения даты
    edit_capacity = State()      # Состояние изменения вместимости
    edit_description = State()   # Состояние изменения описания
    edit_place = State()         # Состояние изменения адреса
    edit_entry = State()         # Состояние изменения сбора гостей
    edit_start = State()         # Состояние изменения начала
    edit_price = State()         # Состояние изменения стоимости


# этот хэндлер будет срабатывать на команду "/start" -
# и отправлять ему стартовое меню
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_cammand(message: Message):
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


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии добавления мероприятия
@router.message(Command(commands='cancel'), StateFilter(FSMAdmin.add_event))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Добавление мероприятия отменено.')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии удаления мероприятия
@router.message(Command(commands='cancel'), StateFilter(FSMAdmin.cancel_event))
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


# Этот хэндлер будет срабатывать на команду /choose
# и переводить бота в состояние ожидания выбора мероприятия
@router.message(Command(commands='choose'), StateFilter(default_state))
async def process_choose_command(message: Message, state: FSMContext):
    events_list = []
    id_list = []
    num = 1
    event_db = select_event_db()
    if len(event_db) != 0:
        for event in event_db:
            try:
                if event['capacity'] == 0 or now_time(f'{event["date"]} {event["start"]}') < datetime.now():
                    if event_date(event["date"]) == date.today():
                        del_event_db(event["id"])
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
            await message.answer("К сожалению на данный момент нету запланированных мероприятий, попробуйте проверить позже.")
        else:
            events = f'\n\n'.join(events_list)
            text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\nЧтобы прервать процесс бронирования введите команду - /cancel"
            await message.answer(text=text, parse_mode='HTML')
            # Устанавливаем состояние ожидания выбора мероприятия
            await state.set_state(FSMFillForm.event_choosing)
            await state.update_data(id_list=id_list)
    else:
        await message.answer("К сожалению на данный момент нету запланированных мероприятий, попробуйте проверить позже.")


# Этот хэндлер будет срабатывать на callback choose
# и переводить бота в состояние ожидания выбора мероприятия
@router.callback_query(Text(text='choose'), StateFilter(default_state))
async def process_choose_command(callback: CallbackQuery, state: FSMContext):
    events_list = []
    id_list = []
    num = 1
    event_db = select_event_db()
    if len(event_db) != 0:
        for event in event_db:
            try:
                if event['capacity'] == 0 or now_time(f'{event["date"]} {event["start"]}') < datetime.now():
                    if event_date(event["date"]) == date.today():
                        del_event_db(event["id"])
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
            await callback.message.answer("К сожалению на данный момент нету запланированных мероприятий, попробуйте проверить позже.")
        else:
            events = f'\n\n'.join(events_list)
            text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\nЧтобы прервать процесс бронирования введите команду - /cancel"
            await callback.message.answer(text=text, parse_mode='HTML')
            # Устанавливаем состояние ожидания выбора мероприятия
            await state.set_state(FSMFillForm.event_choosing)
            await state.update_data(id_list=id_list)
    else:
        await callback.message.answer("К сожалению на данный момент нету запланированных мероприятий, попробуйте проверить позже.")


# Этот хэндлер будет срабатывать, если введен корректный номер мероприятия
@router.message(StateFilter(FSMFillForm.event_choosing),
            lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_event_choosing(message: Message, state: FSMContext):
    db = await state.get_data()
    id_list = db['id_list']
    if int(message.text) in id_list:
        event_db = select_one_event(int(message.text))
        await message.answer(text=f'Вы выбрали мероприятие: "{event_db["name"]}"\n'
                                f'На какое количество гостей вы хотите забронировать места ?\n\n'
                                f'Чтобы прервать процесс бронирования введите команду - /cancel')
        # Cохраняем название мероприятия в хранилище по ключу "event"
        name = event_db['name']
        date = event_db['date']
        place = event_db['place']
        entry = event_db['entry']
        start = event_db['start']
        id = int(event_db['id'])
        await state.update_data(name=name, date=date, place=place, entry=entry, start=start, id=id)
        # Устанавливаем состояние ожидания выбора количества гостей
        await state.set_state(FSMFillForm.guests_choosing)
    else:
        await message.answer(text=f'Введен не верный код мероприятия, попробуйте еще раз\n\n'
                                f'Чтобы прервать процесс бронирования введите команду - /cancel')


# Этот хэндлер будет срабатывать, если во время
# выбора мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.event_choosing))
async def warning_not_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе бронирования мероприятия\n\n'
             f'<i>ДЛЯ ВЫБОРА МЕРОПРИЯТИЯ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\n'
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
async def process_guests_choosing(message: Message, state: FSMContext):
    if check_phone(message.text):
        db = await state.get_data()
        capacity = int(select_capacity_event(db['id']))
        new_capacity = str(capacity - db["guests"])
        edit_capacity_event(new_capacity, db['id'])
        # Добавляем в базу данных бронирование пользователя
        insert_reserv_db(str(message.from_user.id), db['name'], str(db["guests"]),
                         db['date'], db["place"], db['entry'], db['start'],
                          str(message.from_user.full_name), str(message.from_user.username), str(message.text))
        # Завершаем машину состояний
        await state.clear()
        # Отправляем в чат сообщение о бронировании
        await message.answer(
            text=f'Все готово! ✨\nВы забронировали {db["guests"]} мест(а) на "{db["name"]}" {db["date"]} в {db["place"]}\n'
                 f'<b>Время сбора гостей {db["entry"]}</b>\n<b>Начало {db["start"]}\n</b>'
                 f'Пожалуйста, приходите ко времени сбора гостей, чтобы заказать еду и напитки,'
                 f' а также насладиться классной музыкой и атмосферой перед шоу 🍷\n\n'
                 f'<i>Обратите внимание: количество столиков и мест в зале не всегда эквивалентно количеству броней.</i>'
                 f'<i> Для того, чтобы наверняка сидеть вместе со своими друзьями, пожалуйста, приходите ко времени сбора гостей.</i>'
                 f'<i> Иногда мы подсаживаем зрителей друг к другу, чтобы сделать рассадку более театральной.</i>'
                 f'<i> Благодарим за понимание.\n\nЕсли вдруг у тебя остались вопросы, ты можешь написать в личные сообщения tg: @anyashukel</i>\n\n'
                 f'Чтобы отменить бронь введите команду\n/cancelreservation',
                 parse_mode='HTML')
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
        name_list = select_event_name_db()
        names = f', '.join(name_list)
        # Устанавливаем состояние ожидания ввода названия мероприятия
        await state.set_state(FSMAdmin.show_reserv)
        await message.answer(
                text=f'Введите название мероприятия, на которое хотите посмотреть брони\n\n'
                     f'Доступные мероприятия: {names}\n\n'
                     f'Чтобы выйти из процесса просмотра броней, введите команду - /cancel')


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
        name_list = select_event_name_db()
        names = f', '.join(name_list)
        # Устанавливаем состояние ожидания ввода названия мероприятия
        await state.set_state(FSMAdmin.show_reserv)
        await callback.message.answer(
                text=f'Введите название мероприятия, на которое хотите посмотреть брони\n\n'
                     f'Доступные мероприятия: {names}\n\n'
                     f'Чтобы выйти из процесса просмотра броней, введите команду - /cancel')


# Этот хэндлер будет срабатывать, если введено корректное название мероприятия
@router.message(StateFilter(FSMAdmin.show_reserv))
async def process_show_reservation(message: Message, state: FSMContext):
    if message.text in select_event_name_db():
        # Получаем список бронирований
        reserv_list = select_for_admin_reserv_db(message.text)
        if len(reserv_list) != 0:
            capacity = select_capacity_event_db(message.text)
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
            bookings = f'\n\n'.join(booking_list)
            await message.answer(text=f"{bookings}\n\nВсего забронировано мест: {reserved_seats}\nСвободно мест: {capacity}\n\nЧтобы отменить бронь введите команду\n/cancelreservation")
            # Завершаем машину состояний
            await state.clear()
        else:
            await message.answer(f'Брони на "{message.text}" пока что нет.')
            # Завершаем машину состояний
            await state.clear()
    else:
        await message.answer(f'Такого мероприятия не найдено\n\n'
                             'Чтобы выйти из процесса просмотра броней, введите команду - /cancel')


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
        name_list = select_event_name_db()
        names = f', '.join(name_list)
        if len(name_list) != 0:
            # Устанавливаем состояние ожидания ввода названия мероприятия
            await state.set_state(FSMCancelReserv.show_reserv_for_cancel)
            await message.answer(
                    text=f'Введите название мероприятия, на которое хотите отменить бронь\n\n'
                        f'Доступные мероприятия: {names}\n\n'
                        f'Чтобы выйти из процесса отмены броней, введите команду - /cancel')
        else:
            # Если нету активных мероприятий, то оповещвем об этом администратора
            await message.answer('Активных мероприятий пока что нету')


# Этот хэндлер будет срабатывать, если введено корректное название мероприятия
@router.message(StateFilter(FSMCancelReserv.show_reserv_for_cancel))
async def process_show_reservation_for_cancel(message: Message, state: FSMContext):
    if message.text in select_event_name_db():
        # Получаем список бронирований
        reserv_list = select_for_admin_reserv_db(message.text)
        if len(reserv_list) != 0:
            capacity = select_capacity_event_db(message.text)
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
            await message.answer(text=f"{bookings}\n\nВсего забронировано мест: {reserved_seats}\nСвободно мест: {capacity}\n\nЕсли вы хотите прервать процесс отмены брони - отправьте команду /cancel'", parse_mode='HTML')
            # Устанавливаем состояние ожидания ввода кода бронирования
            await state.set_state(FSMCancelReserv.cancel_reservation)
        else:
            await message.answer(f'Брони на "{message.text}" пока что нет')
            # Завершаем машину состояний
            await state.clear()
    else:
        await message.answer(f'Такого мероприятия не найдено, введите название мероприятия еще раз\n\n'
                             'Если вы хотите прервать процесс отмены брони - '
                             'отправьте команду /cancel')


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
    await message.answer(text=LEXICON['add'])
    await state.set_state(FSMAdmin.add_event)


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
            insert_event_db(add_list[0], add_list[1], add_list[2], add_list[3],
                            add_list[4], add_list[5], add_list[6], add_list[7])
            await message.answer('Мероприятие добавлено')
            # Завершаем машину состояний
            await state.clear()
    else:
        await message.answer(f'Введенные данные о мероприятии не корректны\n'
                             f'Скорее всего вы забыли поставить ; в конце одного из разделов или поставили лишний знак ;\n'
                             f'Сравните еще раз введенные данные с шаблоном и после исправления отправьте данные о мероприятии\n\n'
                             f'Если вы хотите прервать процесс добавления мероприятия - '
                             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать на отправку команды /cancelevent
# и отправлять в чат список мероприятий
@router.message(Command(commands='cancelevent'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_delevent_command(message: Message, state: FSMContext):
    events_list = []
    id_list = []
    num = 1
    event_db = select_event_db()
    if len(event_db) != 0:
        for event in event_db:
            events_list.append(f'{num}) "{event["name"]}"\n{event["description"]}\n'
                                f'Дата и время проведения: {event["date"]} в {event["start"]}\n'
                                f'Сбор гостей в {event["entry"]}\n'
                                f'Вход: {event["price"]}\n'
                                f'Адрес: {event["place"]}\n'
                                f'<b>КОД МЕРОПРИЯТИЯ 👉🏻 {event["id"]}</b>')
            id_list.append(event["id"])
            num += 1
        events = f'\n\n'.join(events_list)
        text = f"{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️\n\nЧтобы прервать процесса отмены мероприятия, введите команду - /cancel"
        await message.answer(text=text, parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора мероприятия
        await state.set_state(FSMAdmin.cancel_event)
        await state.update_data(id_list=id_list)
    else:
        await message.answer(text='Мероприятий пока что нет')


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
                    text = f'Дорогой зритель, вынуждены сообщить, что мероприятие "{event["name"]}" И {event["date"]} отменено по техническим причинам.\nПриносим свои извинения и ждем на наших следующих мероприятиях.'
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


# Этот хэндлер будет срабатывать, если во время
# удаления мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMAdmin.cancel_event))
async def del_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе удаления мероприятия\n'
             f'Для удаления мероприятия введите код мероприятия\n'
             'Если вы хотите прервать процесс удаления - '
             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать на отправку команды /editevent
# и отправлять в чат список мероприятий
@router.message(Command(commands='editevent'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_editevent_command(message: Message, state: FSMContext):
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
        await message.answer(text=text, parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора мероприятия
        await state.set_state(FSMEditEvent.choose_event)
    else:
        await message.answer(text='Мероприятий пока что нет')


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
                                start=event["start"], price=event["price"])
        await message.answer(text=f'Вы выбрали мероприятие: {event["name"]}\n\n'
                                f'Отправьте номер раздела, в который хотите внести изменение:\n'
                                f'1 - Название мероприятия\n'
                                f'2 - Дата проведения\n'
                                f'3 - Количество мест\n'
                                f'4 - Краткое описание мероприятия\n'
                                f'5 - Место проведения и адрес\n'
                                f'6 - Сбор гостей\n'
                                f'7 - Начало\n'
                                f'8 - Вход\n\n'
                                f'Чтобы прервать процесса изменения мероприятия, введите команду - /cancel')
        # Устанавливаем состояние ожидания выбора изменения
        await state.set_state(FSMEditEvent.choose_change)
    else:
        await message.answer(f'Введены не корректные данные, чтобы выбрать мероприятие, '
                             f'в которое вы хотите внести изменения, введите код мероприятия\n'
                             f'Если вы хотите прервать процесс редактирования - отправьте команду\n/cancel')


# Этот хэндлер будет срабатывать, если во время
# удаления мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMEditEvent.choose_event))
async def del_event(message: Message):
    await message.answer(f'Введены не корректные данные, чтобы выбрать мероприятие, '
                         f'в которое вы хотите внести изменения, введите код мероприятия\n'
                         f'Если вы хотите прервать процесс редактирования - отправьте команду\n/cancel')


# Этот хэндлер будет выбирать раздел, в который необходимо внести изменения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMEditEvent.choose_change),
lambda x: x.text.isdigit() and 1 <= int(x.text) <= 8)
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
    else:
        await message.answer(f'Введите номер раздела от 1 до 8\n\n'
                             f'Если вы хотите прервать процесс редактирования - '
                             f'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если во время
# редактирования мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMEditEvent.choose_change))
async def edit_event(message: Message):
    await message.answer(f'Введены не корректные данные, чтобы выбрать раздел, '
                         f'в который вы хотите внести изменения, введите номер раздела от 1 до 8\n\n'
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
        edit_name_event(new_name, id)
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
