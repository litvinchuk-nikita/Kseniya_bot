from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


# def create_pag_kb_question(pag) -> InlineKeyboardMarkup:
#     forward_button: InlineKeyboardButton = InlineKeyboardButton(
#         text=LEXICON['forward'], callback_data='forward')
#     backward_button: InlineKeyboardButton = InlineKeyboardButton(
#         text=LEXICON['backward'], callback_data='backward')
#     pag_button: InlineKeyboardButton = InlineKeyboardButton(
#         text=pag, callback_data='pag')
#     menu_button: InlineKeyboardButton = InlineKeyboardButton(
#         text='Вернуться в меню', callback_data='backword_menu')
#     kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
#     kb_builder.add(backward_button, pag_button, forward_button, menu_button)
#     kb_builder.adjust(3, 1)
#     return kb_builder.as_markup()
