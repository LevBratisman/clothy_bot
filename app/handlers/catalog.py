from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ContentType

import asyncio
import os

from app import keyboards
from app.database import get_data


catalog_router = Router()

@catalog_router.message(F.text == "Каталог")
async def catalog(message: Message):
    await message.answer("Выберите категорию", reply_markup=keyboards.catalog)


@catalog_router.message(F.text == "Назад")
async def back_to_manu(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Меню", reply_markup=keyboards.start_admin_keyboard)
    else:
        await message.answer("Меню", reply_markup=keyboards.start_keyboard)
    

@catalog_router.message(F.text == "Избранное")
async def favorite(message: Message):
    await message.answer("Пусто..")
    
@catalog_router.message(F.text == "Корзина")
async def basket(message: Message):
    await message.answer("Пусто..")
    
    
@catalog_router.callback_query(F.data == "shoes")
async def get_shoes(callback: Message):
    await callback.answer("Вы выбрали каталог 'Обувь'")
    data = await get_data("shoes")
    await callback.message.answer('Загружаю товар...')
    await asyncio.sleep(1)
    for item in range(len(data)):
        await asyncio.sleep(0.3)
        await callback.message.answer_photo(data[item][0], caption=f'<b>Тип</b>: {data[item][1]}\n' + 
                                                                    f'<b>Название</b>: {data[item][2]}\n' + 
                                                                    f'<b>Описание</b>: {data[item][3]}\n' +
                                                                    f'<b>Цена</b>: {data[item][4]}', parse_mode='HTML')

    
@catalog_router.callback_query(F.data == "clothes")
async def get_clothes(callback: Message):
    await callback.answer("Вы выбрали каталог 'Одежда'")
    data = await get_data("clothes")
    await callback.message.answer('Загружаю товар...')
    await asyncio.sleep(1)
    for item in range(len(data)):
        await asyncio.sleep(0.3)
        await callback.message.answer_photo(data[item][0], caption=f'<b>Тип</b>: {data[item][1]}\n' + 
                                                                    f'<b>Название</b>: {data[item][2]}\n' + 
                                                                    f'<b>Описание</b>: {data[item][3]}\n' +
                                                                    f'<b>Цена</b>: {data[item][4]}', parse_mode='HTML')
    
    
@catalog_router.callback_query(F.data == "headdress")
async def get_headdress(callback: Message):
    await callback.answer("Вы выбрали каталог 'Головные уборы'")
    data = await get_data("headdress")
    await callback.message.answer('Загружаю товар...')
    await asyncio.sleep(1)
    for item in range(len(data)):
        await asyncio.sleep(0.3)
        await callback.message.answer_photo(data[item][0], caption=f'<b>Тип</b>: {data[item][1]}\n' + 
                                                                    f'<b>Название</b>: {data[item][2]}\n' + 
                                                                    f'<b>Описание</b>: {data[item][3]}\n' +
                                                                    f'<b>Цена</b>: {data[item][4]}', parse_mode='HTML')