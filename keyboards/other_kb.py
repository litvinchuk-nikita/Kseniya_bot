from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_menu_kb() -> InlineKeyboardMarkup:
    choose_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Выбрать мероприятие', callback_data='choose')
    showreserv_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Посмотреть мои активные брони', callback_data='showreservation')
    cancelreserv_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Возможности бота', callback_data='help')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(choose_button, showreserv_button, cancelreserv_button)
    kb_builder.adjust(1, 1, 1)
    return kb_builder.as_markup()
