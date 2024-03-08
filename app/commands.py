from aiogram.types import BotCommand, Message
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app import keyboards
from app.handlers.catalog import catalog

cmd_router = Router()

private = [
    BotCommand(command="start", description="Запустить бота"),
    BotCommand(command="catalog", description="Перейти в каталог"),
    BotCommand(command="about", description="Информация о боте"),
    BotCommand(command="contacts", description="Контакты"),
]

@cmd_router.message(Command("contacts"))
async def contacts(message: Message):
    await message.answer(f"По всем вопросам обращайтесь к @bratisman")
    
@cmd_router.message(Command("about"))
async def about(message: Message):
    await message.answer("Телеграм бот для магазина. Все права защищены")
    
    