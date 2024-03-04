from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ContentType
import asyncio
import os

from app import keyboards
from app.database import add_item_db, get_data, delete_item_db



admin_router = Router()


class NewItem(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()
    brand = State()
    
    
class DelItem(StatesGroup):
    id = State()


@admin_router.message(F.text == "Назад")
async def back_to_manu(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Меню", reply_markup=keyboards.start_admin_keyboard)
    else:
        await message.answer("Меню", reply_markup=keyboards.start_keyboard)
    
    
@admin_router.message(F.text == "Админ-панель")
async def back_to_manu(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Вы вошли в админ-панель", reply_markup=keyboards.admin_panel)
        
        
@admin_router.message(F.text == "Добавить товар")
async def back_to_manu(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await state.set_state(NewItem.type)
        await message.answer("Выберите тип товара", reply_markup=keyboards.catalog)
        
        
@admin_router.message(F.text == "Удалить товар")
async def back_to_manu(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await state.set_state(DelItem.id)
        await message.answer("Укажите код товара:")
        

@admin_router.message(DelItem.id)
async def back_to_manu(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        try: 
            await delete_item_db(int(message.text))
        except ValueError:
            await message.answer("Некорректный формат данных. Попробуйте ещё раз.")
        else:
            await message.answer("Товар был успешно удален!")
            await state.clear()
        
# @admin_router.message(F.text == "Изменить товар")
# async def back_to_manu(message: Message, state: FSMContext):
#     if message.from_user.id == int(os.getenv('ADMIN_ID')):
#         await message.answer("Выберите тип товара")
#         cur_data = get_data_by_id()
#         await message.answer("Выберите тип товара", reply_markup=keyboards.catalog)
        
        
@admin_router.callback_query(NewItem.type)
async def add_item_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(type=callback.data)
    await state.set_state(NewItem.name)
    await callback.message.answer("Теперь введите название")
    
    
@admin_router.message(NewItem.name)
async def add_item_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(NewItem.brand)
    await message.answer("Теперь введите название бренда")
    
    
@admin_router.message(NewItem.brand)
async def add_item_brand(message: Message, state: FSMContext):
    await state.update_data(brand=message.text)
    await state.set_state(NewItem.desc)
    await message.answer("Теперь введите описание товара")
    
    
@admin_router.message(NewItem.desc)
async def add_item_desc(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await state.set_state(NewItem.price)
    await message.answer("Теперь введите цену товара")
    
    
@admin_router.message(NewItem.price)
async def add_item_price(message: Message, state: FSMContext):
    try:
        await state.update_data(price=int(message.text))
    except ValueError:
        await message.answer("Некорректный формат данных. Попробуйте ещё раз.")
    else:
        await state.set_state(NewItem.photo)
        await message.answer("Теперь отправьте фотографию товара")
    
    
@admin_router.message(lambda message: not message.photo, NewItem.photo)
async def check_photo(message: Message):
    await message.answer("Это не фотография!")
    
    
@admin_router.message(F.content_type == ContentType.PHOTO, NewItem.photo)
async def add_item_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id)
    data = await state.get_data()
    await add_item_db(data)
    await message.answer("Товар успешно добавлен!")
    await message.answer(f'Тип: {data["type"]}\nНазвание: {data["name"]}\nОписание: {data["desc"]}\nЦена: {data["price"]}\nБренд: {data["brand"]}, \nФото: {data["photo"]}')
    await state.clear()