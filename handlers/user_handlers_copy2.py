from datetime import datetime, date, timedelta
import requests
from config_data.config import Config, load_config
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.types import CallbackQuery, Message, URLInputFile, InputMediaPhoto, ContentType
from database.database import event_db, user_dict
# from keyboards.pagination_kb import (create_pag_kb_question, create_pag_kb_photo)
from keyboards.other_kb import create_event_kb
from lexicon.lexicon import LEXICON
from filters.filters import IsAdmin

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



# этот хэндлер будет срабатывать на команду "/start" -
# и отправлять ему стартовое меню
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_cammand(message: Message):
    # events_list = []
    # num = 1
    # for event in event_db:
    #     events_list.append(f"{num}) {event['name']}\nДата проведения: {event['date']}")
    #     num += 1
    # events = f'\n\n'.join(events_list)
    # text = f"{LEXICON['/start']}\n\n{events}\n\nЧтобы перейти к выбору мероприятия введите команду - /choose"
    text = f"{LEXICON['/start']}\n\nЧтобы перейти к выбору мероприятия введите команду -\n/choose"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await message.answer_photo(
        photo=photo,
        caption=text)


# этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text=f'Отменять нечего.'
             'Чтобы перейти к выбору мероприятия введите команду /choose')


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии выбора мероприятия и выбора количества гостей
@router.message(Command(commands='cancel'), StateFilter(FSMFillForm.event_choosing, FSMFillForm.guests_choosing))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Бронирование мест отменено.\n\n'
             'Чтобы снова перейти к выбору мероприятия введите команду /choose')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии добавления мероприятия
@router.message(Command(commands='cancel'), StateFilter(FSMAdmin.add_event))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Добавление мероприятия отменено.\n\n')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии удаления мероприятия
@router.message(Command(commands='cancel'), StateFilter(FSMAdmin.del_event))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Удаление мероприятия отменено.\n\n')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel"
# в состоянии отмены бронирования
@router.message(Command(commands='cancel'), StateFilter(FSMCancelReserv.cancel_reservation))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text=f'Отмена бронирования прервана.\n\n')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду /choose
# и переводить бота в состояние ожидания выбора мероприятия
@router.message(Command(commands='choose'), StateFilter(default_state))
async def process_choose_command(message: Message, state: FSMContext):
    events_list = []
    num = 1
    for event in event_db:
        if event['capacity'] == 0:
            continue
        events_list.append(f"{num}) {event['name']}\n{event['description']}\n"
                           f"Дата и время проведения: {event['date']} в {event['start']}\n"
                           f"Cтоимость: {event['price']}")
        num += 1
    events = f'\n\n'.join(events_list)
    text = f"{events}\n\nЧтобы выбрать мероприятие введите номер мероприятия от 1 до {len(event_db)}"
    await message.answer(text=text)
    # Устанавливаем состояние ожидания выбора мероприятия
    await state.set_state(FSMFillForm.event_choosing)


# Этот хэндлер будет срабатывать, если введен корректный номер мероприятия
@router.message(StateFilter(FSMFillForm.event_choosing),
            lambda x: x.text.isdigit() and 1 <= int(x.text) <= len(event_db))
async def process_event_choosing(message: Message, state: FSMContext):
    event = event_db[int(message.text) - 1]['name']
    capacity = event_db[int(message.text) - 1]['capacity']
    await message.answer(text=f'Вы выбрали мероприятие: {event}\n'
                              f'Cвободно мест: {capacity}\n'
                              f'На какое количество гостей вы хотите забронировать места ?')
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
        text=f'Для выбора мероприятия введите номер мероприятия от 1 до {len(event_db)}\n'
             'Если вы хотите прервать бронирование - '
             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если введено корректное число гостей
@router.message(StateFilter(FSMFillForm.guests_choosing),
            lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_guests_choosing(message: Message, state: FSMContext):
    capacity = None
    db = await state.get_data()
    for event in event_db:
        if event['name'] ==  db['event']:
            capacity = event['capacity']
    if int(message.text) <= capacity:
        # Cохраняем количество гостей в хранилище по ключу "guests"
        guests = int(message.text)
        await state.update_data(guests=guests)
        for i in range(len(event_db)):
            if event_db[i]['name'] ==  db['event']:
                event_db[i]['capacity'] -= int(message.text)
        print(event_db)
        # Добавляем в "базу данных" бронирование пользователя
        # по ключу id пользователя
        if message.from_user.id not in user_dict:
            user_dict[message.from_user.id] = []
        user_dict[message.from_user.id].append(await state.get_data())

        # Завершаем машину состояний
        await state.clear()
        # Отправляем в чат сообщение о бронировании
        await message.answer(
            text=f'Все готово!\nНапоминаю, что время сбора гостей {db["entry"]}\nНачало {db["start"]}\n'
                 f'Пожалуйста, приходи ко времени сбора гостей, чтобы заказать еду и напитки\n'
                 f'Если вдруг у тебя остались вопросы, ты можешь написать Ане в личные сообщения\n'
                 f'tg: @anyashukel')
    else:
        await message.answer(f'К сожалению столько свободных мест нету,'
                             f' выберети количество мест не привышающее {capacity}\n'
                             'Если вы хотите прервать бронирование - '
                             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если во время
# выбора количества гостей введено что-то некорректное
@router.message(StateFilter(FSMFillForm.guests_choosing))
async def warning_not_guests(message: Message):
    await message.answer(
        text=f'Для выбора количества гостей введите цифру от 1\n'
             'Если вы хотите прервать бронирование - '
             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать на отправку команды /showreservation
# и отправлять в чат данные о бронировании, либо сообщение об отсутствии данных
@router.message(Command(commands='showreservation'), StateFilter(default_state))
async def process_showreservation_command(message: Message):
    # Отправляем пользователю информацию о бронировании, если оно есть в "базе данных"
    if message.from_user.id in user_dict:
        booking_list = []
        num = 1
        for booking in user_dict[message.from_user.id]:
            booking_list.append(f'{num}) {booking["event"]}'
                                f' на {booking["guests"]} гостей.\n'
                                f'Дата проведения: {booking["date"]}\n'
                                f'Место проведения: {booking["place"]}\n'
                                f'Вход в {booking["entry"]}, начало в {booking["start"]}')
            num += 1
        bookings = f'\n\n'.join(booking_list)
        await message.answer(text=f"Забронированные мероприятия:\n{bookings}")
    else:
        # Если бронирования в базе нет - предлагаем звыбрать
        await message.answer(
            text=f'У вас пока что нету бронирований.\n'
                 'Чтобы перейти к выбору мероприятия введите команду /choose')


# Этот хэндлер будет срабатывать на отправку команды /cancelreservation
# и отправлять в чат данные о бронировании и вопрос о снятии бронирования
@router.message(Command(commands='cancelreservation'), StateFilter(default_state))
async def process_cancelreservation_command(message: Message, state: FSMContext):
    # Отправляем пользователю информацию о бронировании, если оно есть в "базе данных"
    if message.from_user.id in user_dict:
        booking_list = []
        num = 1
        for booking in user_dict[message.from_user.id]:
            booking_list.append(f'{num}) {booking["event"]}'
                                f' на {booking["guests"]} гостей.\n'
                                f'Дата проведения: {booking["date"]}\n'
                                f'Место проведения: {booking["place"]}\n'
                                f'Вход в {booking["entry"]}, начало в {booking["start"]}')
            num += 1
        bookings = f'\n\n'.join(booking_list)
        await message.answer(text=f'Забронированные мероприятия:\n{bookings}\n'
                                  f'Для отмены бронирования введите номер бронирования')
        # Устанавливаем состояние ожидания выбора отмены бронирования
        await state.set_state(FSMCancelReserv.cancel_reservation)
    else:
        # Если бронирования в базе нет - предлагаем перейти к выбору мероприятия
        await message.answer(
            text=f'У вас пока что нету бронирований.\n'
                 'Чтобы перейти к выбору мероприятия введите команду /choose')


# Этот хэндлер будет срабатывать, если введено корректный номер бронирования
@router.message(StateFilter(FSMCancelReserv.cancel_reservation),
            lambda x: x.text.isdigit() and 1 <= int(x.text))
async def process_cancel_reservation(message: Message, state: FSMContext):
    if int(message.text) <= len(user_dict[message.from_user.id]):
        for i in range(len(event_db)):
            if event_db[i]['name'] ==  user_dict[message.from_user.id][int(message.text) - 1]['event']:
                event_db[i]['capacity'] += user_dict[message.from_user.id][int(message.text) - 1]['guests']
                print(event_db[i]['capacity'])
        user_dict[message.from_user.id].pop(int(message.text) - 1)
        if len(user_dict[message.from_user.id]) == 0:
            user_dict.pop(message.from_user.id)
        # Завершаем машину состояний
        await state.clear()
        # Отправляем в чат сообщение о бронировании
        await message.answer(
            text=f'Бронирование отменено\nЧтобы перейти к выбору мероприятия введите команду /choose')
    else:
        await message.answer(f'Введеное число привышает количество ваших бронирований\n'
                             'Если вы хотите прервать бронирование - '
                             'отправьте команду /cancel')


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
    print(add_list)
    if len(add_list) == 8:
        event_db.append({'name': add_list[0],
                        'date': add_list[1],
                        'capacity': int(add_list[2]),
                        'description': add_list[3],
                        'place': add_list[4],
                        'entry': add_list[5],
                        'start': add_list[6],
                        'price': add_list[7]})
        print(event_db)
        await message.answer('Мероприятие добавлено')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer('Введенные данные о мероприятии не корректны. Введите данные согласно образца.')


# Этот хэндлер будет срабатывать на отправку команды /delevent
# и отправлять в чат список мероприятий
@router.message(Command(commands='delevent'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_delevent_command(message: Message, state: FSMContext):
    events_list = []
    num = 1
    for event in event_db:
        events_list.append(f"{num}) {event['name']}\n{event['description']}\n"
                           f"Дата и время проведения: {event['date']} в {event['start']}")
        num += 1
    events = f'\n\n'.join(events_list)
    text = f"{events}\n\nЧтобы удалить мероприятие введите номер мероприятия от 1 до {len(event_db)}"
    await message.answer(text=text)
    # Устанавливаем состояние ожидания выбора мероприятия
    await state.set_state(FSMAdmin.del_event)


# Этот хэндлер будет удалять мероприятие
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMAdmin.del_event),
lambda x: x.text.isdigit() and 1 <= int(x.text) <= len(event_db))
async def process_add_event(message: Message, state: FSMContext):
    event_db.pop(int(message.text) - 1)
    await message.answer('Мероприятие удалено')
    # Завершаем машину состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если во время
# удаления мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMAdmin.del_event))
async def del_event(message: Message):
    await message.answer(
        text=f'Для удаления мероприятия введите номер мероприятия от 1 до {len(event_db)}\n'
             'Если вы хотите прервать удаление - '
             'отправьте команду /cancel')


# # Этот хэндлер будет срабатывать на нажатие кнопки при
# # подтвержении выбранного мероприятия
# @router.callback_query(StateFilter(FSMFillForm.event_choosing),
#                    Text(text=['no', 'yes']))
# async def process_event_press(callback: CallbackQuery, state: FSMContext):
#     if callback.data == 'yes':

#     # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
#     # по ключу "gender"
#     await state.update_data(gender=callback.data)
#     # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото
#     # чтобы у пользователя не было желания тыкать кнопки
#     await callback.message.delete()
#     await callback.message.answer(
#         text='Спасибо! А теперь загрузите, пожалуйста, ваше фото'
#     )