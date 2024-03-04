from aiogram import Dispatcher, Bot, F
from aiogram.enums import ContentType
from aiogram.types import Message

import asyncio, os
import logging
from dotenv import find_dotenv, load_dotenv

from app.handlers.user_private import user_private_router
from app.handlers.catalog import catalog_router
from app.handlers.admin import admin_router
from app.database import db_start


load_dotenv(find_dotenv())

dp = Dispatcher()
bot = Bot(os.getenv('TOKEN'))



async def on_startup():
    await db_start()

async def main():
    dp.include_router(admin_router)
    dp.include_router(catalog_router)
    dp.include_router(user_private_router)
    # await bot.set_my_commands(private)
    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("error")