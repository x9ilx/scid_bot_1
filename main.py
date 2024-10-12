# Регистрация хендлеров
import asyncio
import logging

# aiogram - асинхронная библиотека для Telegram API
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties

from config import bot_token
from routers import router as main_router


async def main():
    # Устанавливаем уровень логирования
    logging.basicConfig(level=logging.INFO)

    # Создаем бота с сессией и настройками по умолчанию
    bot = Bot(
        token=bot_token,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Создаем диспетчер и подключаем маршрутизатор для обработки событий
    dp = Dispatcher()
    dp.include_router(main_router)

    # Запускаем поллинг для приема сообщений от Telegram
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
