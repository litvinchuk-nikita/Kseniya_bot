import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from aiogram.fsm.storage.redis import RedisStorage, Redis
from handlers import user_handlers, other_handlers
from apsched.apsched import send_message_cron
from keyboards.main_menu import set_main_menu
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

# инициализируем логгер
logger = logging.getLogger(__name__)


# функция конфигурирования и запуска бота
async def main():
    # конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем Redis
    redis = Redis(host='localhost')

    # Инициализируем хранилище
    storage = RedisStorage(redis=redis)

    # инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(storage=storage)

    # # инициализируем scheduler
    scheduler = AsyncIOScheduler(timezone='Europe/Kaliningrad')
    scheduler.add_job(send_message_cron, trigger='cron', hour=12,
                    minute=00, start_date=datetime.now(), kwargs={'bot': bot})

    # настраиваем главное меню бота
    await set_main_menu(bot)

    # регестрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # запускаем scheduler
    scheduler.start()
    # запускаем polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
