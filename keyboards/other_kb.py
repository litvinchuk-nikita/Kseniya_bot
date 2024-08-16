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
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(choose_button, showreserv_button, cancelreserv_button, review_button)
    kb_builder.adjust(1, 1, 1, 1)
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