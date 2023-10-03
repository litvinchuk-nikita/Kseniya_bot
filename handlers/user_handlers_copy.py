from datetime import datetime, date, timedelta
import requests
from config_data.config import Config, load_config
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.types import CallbackQuery, Message, URLInputFile, InputMediaPhoto, ContentType
from database.database import event_db, user_db
# from keyboards.pagination_kb import (create_pag_kb_question, create_pag_kb_photo)
# from keyboards.other_kb import (create_menu_kb, create_info_kb, create_date_kb,
#                                 create_time_kb, create_confirmation_kb, create_pay_kb)
from lexicon.lexicon import LEXICON

router: Router = Router()


# загружаем конфиг в переменную config
config: Config = load_config()


# этот хэндлер будет срабатывать на команду "/start" -
# и отправлять ему стартовое меню
@router.message(CommandStart())
async def process_start_cammand(message: Message):
    events_list = []
    num = 1
    for event in event_db:
        events_list.append(f"{num}) {event['name']}\nДата проведения: {event['date']}")
        num += 1
    events = f'\n\n'.join(events_list)
    text = f"{LEXICON['/start']}\n\n{events}"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await message.answer_photo(
        photo=photo,
        caption=text)


# этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])