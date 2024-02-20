from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

import asyncio



user_private_router = Router()

@user_private_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Приветствую, {message.from_user.full_name}!")
    await asyncio.sleep(1)
    await message.answer(f"Добро пожаловать в тур-агенство Balibu!")
    
@user_private_router.message()
async def text(message: Message):
    await message.reply("Извините, я не понимаю")