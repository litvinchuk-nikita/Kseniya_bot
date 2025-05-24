from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_menu_kb() -> InlineKeyboardMarkup:
    choose_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Выбрать мероприятие', callback_data='choose')
    showreserv_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Посмотреть мои активные брони', callback_data='showreservation')
    cancelreserv_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Возможности бота', callback_data='help')
    review_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Оставить отзыв', callback_data='review')
    draw_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Участвовать в розыгрыше', callback_data='draw')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(choose_button, showreserv_button, draw_button, cancelreserv_button, review_button)
    kb_builder.adjust(1, 1, 1, 1, 1)
    return kb_builder.as_markup()


def review_kb() -> InlineKeyboardMarkup:
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Анонимно', callback_data='anonim')
    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Не анонимно', callback_data='not_anonim')
    button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить отправку отзыва', callback_data='cancel_review')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(button_1, button_2, button_3)
    kb_builder.adjust(1, 1, 1)
    return kb_builder.as_markup()


def send_review_kb() -> InlineKeyboardMarkup:
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Редактировать отзыв', callback_data='edit_review')
    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Отправить отзыв', callback_data='send_review')
    button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить отправку отзыва', callback_data='cancel_review')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(button_1, button_2, button_3)
    kb_builder.adjust(1, 1, 1)
    return kb_builder.as_markup()


def send_answer_kb() -> InlineKeyboardMarkup:
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Редактировать ответ на отзыв', callback_data='edit_answer')
    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Отправить ответ на отзыв', callback_data='send_answer')
    button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить отправку ответа на отзыва', callback_data='cancel_answer')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(button_1, button_2, button_3)
    kb_builder.adjust(1, 1, 1)
    return kb_builder.as_markup()


def send_review_kb_2() -> InlineKeyboardMarkup:
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Редактировать отзыв', callback_data='edit_review')
    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Редактировать имя', callback_data='edit_name')
    button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Редактировать номер телефона', callback_data='edit_phone')
    button_4: InlineKeyboardButton = InlineKeyboardButton(
        text='Отправить отзыв', callback_data='send_review')
    button_5: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить отправку отзыва', callback_data='cancel_review')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(button_1, button_2, button_3, button_4, button_5)
    kb_builder.adjust(1, 1, 1, 1, 1)
    return kb_builder.as_markup()

def answer_review_kb() -> InlineKeyboardMarkup:
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Ответить на отзыв', callback_data='answer_review')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(button_1)
    return kb_builder.as_markup()

def cancel_review_kb() -> InlineKeyboardMarkup:
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить отправку отзыва', callback_data='cancel_review')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(button_1)
    return kb_builder.as_markup()

def cancel_answer_kb() -> InlineKeyboardMarkup:
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить отправку ответа на отзыв', callback_data='cancel_answer')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(button_1)
    return kb_builder.as_markup()


def last_review_kb() -> InlineKeyboardMarkup:
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Оставить еще один отзыв', callback_data='review')
    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Вернуться в главное меню', callback_data='menu')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(button_1, button_2)
    kb_builder.adjust(1, 1)
    return kb_builder.as_markup()


def newsletter_kb() -> InlineKeyboardMarkup:
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Выбрать мероприятие для рассылки', callback_data='nl_event')
    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Отправить независимую рассылку', callback_data='nl_not_event')
    button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить отправку рассылки', callback_data='cancel_nl')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(button_1, button_2, button_3)
    kb_builder.adjust(1, 1, 1)
    return kb_builder.as_markup()


def draw_kb() -> InlineKeyboardMarkup:
    draw_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Участвовать в розыгрыше', callback_data='draw')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(draw_button)
    return kb_builder.as_markup()


def choose_event_kb() -> InlineKeyboardMarkup:
    bot_event_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Мероприятия доступные в боте', callback_data='bot_event')
    other_event_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Мероприятия на сторонних площадках', callback_data='other_event')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(bot_event_button, other_event_button)
    kb_builder.adjust(1, 1)
    return kb_builder.as_markup()


def choose_add_event_kb() -> InlineKeyboardMarkup:
    bot_event_button: InlineKeyboardButton = InlineKeyboardButton(
        text='С бронью зрительских мест', callback_data='bot_add_event')
    other_event_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Со ссылкой на покупку билетов', callback_data='other_add_event')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(bot_event_button, other_event_button)
    kb_builder.adjust(1, 1)
    return kb_builder.as_markup()

def choose_edit_event_kb() -> InlineKeyboardMarkup:
    bot_event_button: InlineKeyboardButton = InlineKeyboardButton(
        text='С бронью зрительских мест', callback_data='bot_edit_event')
    other_event_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Со ссылкой на покупку билетов', callback_data='other_edit_event')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(bot_event_button, other_event_button)
    kb_builder.adjust(1, 1)
    return kb_builder.as_markup()

def choose_cancel_event_kb() -> InlineKeyboardMarkup:
    bot_event_button: InlineKeyboardButton = InlineKeyboardButton(
        text='С бронью зрительских мест', callback_data='bot_cancel_event')
    other_event_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Со ссылкой на покупку билетов', callback_data='other_cancel_event')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(bot_event_button, other_event_button)
    kb_builder.adjust(1, 1)
    return kb_builder.as_markup()


def url_event_kb(url) -> InlineKeyboardMarkup:
    url_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Купить билеты', url=url)
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(url_button)
    return kb_builder.as_markup()

def create_pag_kb(pag, event_id) -> InlineKeyboardMarkup:
    event_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Забронировать места', callback_data=event_id)
    forward_button: InlineKeyboardButton = InlineKeyboardButton(
        text='>>', callback_data='forward')
    backward_button: InlineKeyboardButton = InlineKeyboardButton(
        text='<<', callback_data='backward')
    pag_button: InlineKeyboardButton = InlineKeyboardButton(
        text=pag, callback_data='pag')
    cancel_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить бронирование', callback_data='cancel')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(event_button, backward_button,
                   pag_button, forward_button, cancel_button)
    kb_builder.adjust(1, 3, 1)
    return kb_builder.as_markup()


def create_pag_kb_url(pag, url) -> InlineKeyboardMarkup:
    event_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Купить билеты', url=url, callback_data='event_url')
    forward_button: InlineKeyboardButton = InlineKeyboardButton(
        text='>>', callback_data='forward')
    backward_button: InlineKeyboardButton = InlineKeyboardButton(
        text='<<', callback_data='backward')
    pag_button: InlineKeyboardButton = InlineKeyboardButton(
        text=pag, callback_data='pag')
    cancel_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить бронирование', callback_data='cancel')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(event_button, backward_button,
                   pag_button, forward_button, cancel_button)
    kb_builder.adjust(1, 3, 1)
    return kb_builder.as_markup()