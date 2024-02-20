from aiogram import Dispatcher, Bot

import asyncio, os
import logging
from dotenv import find_dotenv, load_dotenv

from app.handlers.user_private import user_private_router


load_dotenv(find_dotenv())

dp = Dispatcher()
bot = Bot(os.getenv('TOKEN'))


async def main():
    dp.include_router(user_private_router)
    # await bot.set_my_commands(private)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("error")