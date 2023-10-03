import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import user_handlers, other_handlers
from keyboards.main_menu import set_main_menu

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

    # инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    # настраиваем главное меню бота
    await set_main_menu(bot)

    # регестрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # запускаем polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
