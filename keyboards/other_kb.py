from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_menu_kb() -> InlineKeyboardMarkup:
    choose_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Выбрать мероприятие', callback_data='choose')
    showreserv_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Посмотреть бронирования', callback_data='showreservation')
    cancelreserv_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить бронирование', callback_data='cancelreservation')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(choose_button, showreserv_button, cancelreserv_button)
    kb_builder.adjust(1, 1, 1)
    return kb_builder.as_markup()

def create_cancel_kb() -> InlineKeyboardMarkup:
    button: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить', callback_data='cancel')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(button)
    return kb_builder.as_markup()
