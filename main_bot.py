import sys
import os

# Принудительно задаем корень проекта для импорта папок
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv

# Импортируем только роутер с кнопками из папки handlers
from handlers.iphones import iphones_router

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

async def on_startup():
    print("Бот запущен и готов к работе!")

async def main():
    dp.startup.register(on_startup)
    dp.include_router(iphones_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
