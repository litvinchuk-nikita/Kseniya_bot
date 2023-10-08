from datetime import datetime, date, timedelta
import requests
from config_data.config import Config, load_config
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.types import CallbackQuery, Message, URLInputFile, InputMediaPhoto, ContentType
from database.database import (event_list, insert_event_db, insert_reserv_db, del_event_db,
                               select_event_db, select_reserv_db, update_event_db, del_reserv_db,
                               select_capacity_event_db, select_for_admin_reserv_db, select_event_name_db)
from keyboards.other_kb import create_menu_kb
from lexicon.lexicon import LEXICON
from filters.filters import IsAdmin
from services.file_handling import now_time

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


class FSMCancelReserv(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    cancel_reservation = State()       # Состояние отмены бронирования


class FSMAdmin(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    add_event = State()       # Состояние добавления мероприятия
    del_event = State()       # Состояние добавления мероприятия
    show_reserv = State()     # Состояние просмотра брони на мероприятие


# этот хэндлер будет срабатывать на команду "/start" -
# и отправлять ему стартовое меню
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_cammand(message: Message):
    # print(message.from_user.full_name, message.from_user.id)
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
@router.message(Command(commands='cancel'), StateFilter(FSMFillForm.event_choosing, FSMFillForm.guests_choosing))
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
@router.message(Command(commands='cancel'), StateFilter(FSMAdmin.del_event))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Удаление мероприятия отменено.')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии отмены бронирования
@router.message(Command(commands='cancel'), StateFilter(FSMCancelReserv.cancel_reservation))
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


# Этот хэндлер будет срабатывать на команду /choose
# и переводить бота в состояние ожидания выбора мероприятия
@router.message(Command(commands='choose'), StateFilter(default_state))
async def process_choose_command(message: Message, state: FSMContext):
    events_list = []
    num = 1
    event_db = select_event_db(event_list)
    if len(event_db) != 0:
        for event in event_db:
            if event['capacity'] == 0 or now_time(f'{event["date"]} {event["start"]}') < datetime.now():
                continue
            events_list.append(f'{num}) "{event["name"]}"\n{event["description"]}\n'
                            f'Дата и время проведения: {event["date"]} в {event["start"]}\n'
                            f'Сбор гостей в {event["entry"]}\n'
                            f'Вход: {event["price"]}\n'
                            f'Адрес: {event["place"]}')
            num += 1
        events = f'\n\n'.join(events_list)
        text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ НОМЕР МЕРОПРИЯТИЯ ОТ 1 ДО {len(events_list)}</i>\n\nЧтобы прервать процесс бронирования введите команду - /cancel"
        await message.answer(text=text, parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора мероприятия
        await state.set_state(FSMFillForm.event_choosing)
    else:
        await message.answer("К сожалению на данный момент нету запланированных мероприятий, попробуйте проверить позже.")


# Этот хэндлер будет срабатывать на callback choose
# и переводить бота в состояние ожидания выбора мероприятия
@router.callback_query(Text(text='choose'), StateFilter(default_state))
async def process_choose_command(callback: CallbackQuery, state: FSMContext):
    events_list = []
    num = 1
    event_db = select_event_db(event_list)
    if len(event_db) != 0:
        for event in event_db:
            if event['capacity'] == 0 or now_time(f'{event["date"]} {event["start"]}') < datetime.now():
                continue
            events_list.append(f'{num}) "{event["name"]}"\n{event["description"]}\n'
                            f'Дата и время проведения: {event["date"]} в {event["start"]}\n'
                            f'Сбор гостей в {event["entry"]}\n'
                            f'Вход: {event["price"]}\n'
                            f'Адрес: {event["place"]}')
            num += 1
        events = f'\n\n'.join(events_list)
        text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ НОМЕР МЕРОПРИЯТИЯ ОТ 1 ДО {len(events_list)}</i>\n\nЧтобы прервать процесс бронирования введите команду - /cancel"
        await callback.message.answer(text=text, parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора мероприятия
        await state.set_state(FSMFillForm.event_choosing)
    else:
        await callback.message.answer("К сожалению на данный момент нету запланированных мероприятий, попробуйте проверить позже.")


# Этот хэндлер будет срабатывать, если введен корректный номер мероприятия
@router.message(StateFilter(FSMFillForm.event_choosing),
            lambda x: x.text.isdigit() and 1 <= int(x.text) <= len(select_event_db(event_list)))
async def process_event_choosing(message: Message, state: FSMContext):
    event_db = select_event_db(event_list)
    for event in event_db:
        if event['capacity'] == 0 or now_time(f'{event["date"]} {event["start"]}') < datetime.now():
            event_db.remove(event)
    event = event_db[int(message.text) - 1]['name']
    capacity = event_db[int(message.text) - 1]['capacity']
    await message.answer(text=f'Вы выбрали мероприятие: "{event}"\n'
                              f'На какое количество гостей вы хотите забронировать места ?\n\n'
                              f'Чтобы прервать процесс бронирования введите команду - /cancel')
    # Cохраняем название мероприятия в хранилище по ключу "event"
    event = event_db[int(message.text) - 1]['name']
    date = event_db[int(message.text) - 1]['date']
    place = event_db[int(message.text) - 1]['place']
    entry = event_db[int(message.text) - 1]['entry']
    start = event_db[int(message.text) - 1]['start']
    await state.update_data(event=event, date=date, place=place, entry=entry, start=start)
    # Устанавливаем состояние ожидания выбора количества гостей
    await state.set_state(FSMFillForm.guests_choosing)


# Этот хэндлер будет срабатывать, если во время
# выбора мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.event_choosing))
async def warning_not_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе бронирования мероприятия\n\n'
             f'<i>ДЛЯ ВЫБОРА МЕРОПРИЯТИЯ ВВЕДИТЕ НОМЕР МЕРОПРИЯТИЯ</i>\n\n'
             'Если вы хотите прервать бронирование - '
             'отправьте команду /cancel', parse_mode='HTML')


# Этот хэндлер будет срабатывать, если введено корректное число гостей
@router.message(StateFilter(FSMFillForm.guests_choosing),
            lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_guests_choosing(message: Message, state: FSMContext):
    db = await state.get_data()
    capacity = int(select_capacity_event_db(db['event']))
    if int(message.text) <= capacity:
        # Cохраняем количество гостей в переменную guests
        guests = int(message.text)
        new_capacity = str(capacity - guests)
        update_event_db(new_capacity, db['event'])
        # Добавляем в базу данных бронирование пользователя
        print(str(message.from_user.full_name), str(message.from_user.username))
        insert_reserv_db(str(message.from_user.id), db['event'], str(guests),
                         db['date'], db["place"], db['entry'], db['start'],
                          str(message.from_user.full_name), str(message.from_user.username))
        # Завершаем машину состояний
        await state.clear()
        # Отправляем в чат сообщение о бронировании
        await message.answer(
            text=f'Все готово! ✨\nВы забронировали {guests} мест(а) на "{db["event"]}" {db["date"]} в {db["place"]}\n'
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
        await message.answer(f'К сожалению столько свободных мест нету,'
                             f' выберети количество мест не привышающее {capacity}\n\n'
                             'Если вы хотите прервать бронирование - '
                             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если во время
# выбора количества гостей введено что-то некорректное
@router.message(StateFilter(FSMFillForm.guests_choosing))
async def warning_not_guests(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе бронирования мероприятия\n\n'
             f'<i>ДЛЯ ВЫБОРА КОЛИЧЕСТВА ГОСТЕЙ ВВЕДИТЕ ЦИФРУ ОТ 1</i>\n\n'
             'Если вы хотите прервать бронирование - '
             'отправьте команду /cancel', parse_mode='HTML')


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
            # Если бронирования в базе нет - предлагаем выбрать
            await message.answer(
                text=f'У вас пока что нет активной брони\n\n')
    else:
        # Устанавливаем состояние ожидания ввода названия мероприятия
        await state.set_state(FSMAdmin.show_reserv)
        await message.answer(
                text=f'Введите название мероприятия, на которое хотите посмотреть брони\n\n'
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
        # Устанавливаем состояние ожидания ввода названия мероприятия
        await state.set_state(FSMAdmin.show_reserv)
        await callback.message.answer(
                text=f'Введите название мероприятия, на которое хотите посмотреть брони\n\n'
                     f'Чтобы выйти из процесса просмотра броней, введите команду - /cancel')


# Этот хэндлер будет срабатывать, если введено корректное название мероприятия
@router.message(StateFilter(FSMAdmin.show_reserv))
async def process_cancel_reservation(message: Message, state: FSMContext):
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
                                    f'{booking["guests"]} мест на "{booking["event"]}"\n'
                                    f'tg: @{booking["email"]}')
                num += 1
                reserved_seats += int(booking["guests"])
            bookings = f'\n\n'.join(booking_list)
            await message.answer(text=f"{bookings}\n\nВсего забронировано мест: {reserved_seats}\nСвободно мест: {capacity}")
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
        await message.answer(text=f'<b>ЗАБРОНИРОВАННЫЕ МЕРОПРИЯТИЯ</b>\n\n{bookings}\n\n'
                                  f'<i>ДЛЯ ОТМЕНЫ БРОНИ ВВЕДИТЕ НОМЕР БРОНИРОВАНИЯ</i>\n\n'
                                  f'Если вы хотите прервать процесс отмены брони - '
                                  f'отправьте команду /cancel',
                            parse_mode='HTML')
        # Устанавливаем состояние ожидания выбора отмены бронирования
        await state.set_state(FSMCancelReserv.cancel_reservation)
    else:
        # Если бронирования в базе нет - предлагаем перейти к выбору мероприятия
        await message.answer(
            text=f'У вас пока что нет активной брони.')


# Этот хэндлер будет срабатывать, если введен корректный номер бронирования
@router.message(StateFilter(FSMCancelReserv.cancel_reservation),
            lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_cancel_reservation(message: Message, state: FSMContext):
    # Получаем список бронирований
    reserv_list = select_reserv_db(str(message.from_user.id))
    # Проверям корректность введенных данных
    if int(message.text) <= len(reserv_list):
        try:
            # Получаем количество свободных мест на мероприятие и добавляем количество отмененных мест
            new_capacity = int(select_capacity_event_db(reserv_list[int(message.text) - 1]['event']))
            new_capacity += int(reserv_list[int(message.text) - 1]['guests'])
            # Обновляем количество мест на мероприятие
            update_event_db(str(new_capacity), reserv_list[int(message.text) - 1]['event'])
        except:
            print('Данное мероприятие уже удалено из БД')
        finally:
            # Удаляем бронирование
            del_reserv_db(str(message.from_user.id), reserv_list[int(message.text) - 1]['id'])
            # Завершаем машину состояний
            await state.clear()
            # Отправляем в чат сообщение об отмене бронирования
            await message.answer(
                text=f'Бронирование отменено')
    else:
        await message.answer(f'Введеное число привышает количество ваших бронирований\n\n'
                             'Если вы хотите прервать бронирование - '
                             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если во время
# отмены бронирования будет введено что-то некорректное
@router.message(StateFilter(FSMCancelReserv.cancel_reservation))
async def del_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе отмены брони\n\n'
             f'<i>ДЛЯ ОТМЕНЫ БРОНИ ВВЕДИТЕ НОМЕР БРОНИРОВАНИЯ</i>\n\n'
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
        insert_event_db(add_list[0], add_list[1], add_list[2], add_list[3],
                        add_list[4], add_list[5], add_list[6], add_list[7])
        await message.answer('Мероприятие добавлено')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer('Введенные данные о мероприятии не корректны. Введите данные согласно шаблона.')


# Этот хэндлер будет срабатывать на отправку команды /delevent
# и отправлять в чат список мероприятий
@router.message(Command(commands='delevent'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_delevent_command(message: Message, state: FSMContext):
    events_list = []
    num = 1
    event_db = select_event_db(event_list)
    for event in event_db:
        events_list.append(f'{num}) "{event["name"]}"\n{event["description"]}\n'
                            f'Дата и время проведения: {event["date"]} в {event["start"]}\n'
                            f'Сбор гостей в {event["entry"]}\n'
                            f'Вход: {event["price"]}\n'
                            f'Адрес: {event["place"]}')
        num += 1
    events = f'\n\n'.join(events_list)
    text = f"{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ НОМЕР МЕРОПРИЯТИЯ ОТ 1 ДО {len(event_db)}</i>\n\nЧтобы прервать процесса удаления мероприятия, введите команду - /cancel"
    await message.answer(text=text, parse_mode='HTML')
    # Устанавливаем состояние ожидания выбора мероприятия
    await state.set_state(FSMAdmin.del_event)


# Этот хэндлер будет удалять мероприятие
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMAdmin.del_event),
lambda x: x.text.isdigit() and 1 <= int(x.text) <= len(select_event_db(event_list)))
async def process_add_event(message: Message, state: FSMContext):
    event_db = select_event_db(event_list)
    del_event_db(event_db[int(message.text) - 1]['name'], event_db[int(message.text) - 1]['id'])
    await message.answer('Мероприятие удалено')
    # Завершаем машину состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если во время
# удаления мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMAdmin.del_event))
async def del_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе удаления мероприятия\n'
             f'Для удаления мероприятия введите номер мероприятия от 1 до {len(select_event_db(event_list))}\n'
             'Если вы хотите прервать процесс удаления - '
             'отправьте команду /cancel')