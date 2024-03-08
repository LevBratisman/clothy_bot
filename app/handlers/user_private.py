from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ContentType

import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from app import keyboards
from app.database import cmd_start_db

load_dotenv(find_dotenv())

user_private_router = Router()


@user_private_router.message(CommandStart())
async def cmd_start(message: Message):
    await cmd_start_db(message.from_user.id, message.from_user.full_name)
    await message.answer_sticker("CAACAgIAAxkBAAPcZeMQ9b0YV0b-rpVfAzL9-Uz1LN4AAlQAA0G1Vgxqt_jHCI0B-jQE")
    await asyncio.sleep(1)
    await message.answer(f"Приветствую, {message.from_user.full_name}!")
    await asyncio.sleep(0.5)
    await message.answer(f'Добро пожаловать в интернет-магазин <b>Clothy</b>!\n' +
                         f'Для выбора товара перейдите в <b>КАТАЛОГ</b>⬇️', 
                         reply_markup=keyboards.start_keyboard, parse_mode='HTML')
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Вы авторизировались как Администратор", 
                             reply_markup=keyboards.start_admin_keyboard)
        
        

@user_private_router.message(F.content_type == ContentType.STICKER)
async def contacts(message: Message):
    await message.answer(message.sticker.file_id)
        
    
@user_private_router.message(F.text == "👨‍💻Контакты")
async def contacts(message: Message):
    await message.answer(f"По всем вопросам обращайтесь к @bratisman")
    
    
@user_private_router.message(F.text == "id")
async def contacts(message: Message):
    await message.answer(f'Ваш id: {message.from_user.id}')

    
@user_private_router.message()
async def text(message: Message):
    await message.reply("Извините, я не понимаю")