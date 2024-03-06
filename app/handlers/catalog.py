from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.enums import ContentType
import json

import asyncio
import os

from app import keyboards
from app.database import get_data_by_type, get_user_data_by_user_id, add_item_to_cart_db, get_data_by_id, update_cart_id


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
    

    
@catalog_router.message(F.text == "Корзина")
async def basket(message: Message):
    data = await get_user_data_by_user_id(message.from_user.id)
    prev_cart = data[4]
    if prev_cart is None:
        await message.answer("Корзина пуста")
    else:
        prev_cart = prev_cart.split(', ')
        for i in range(len(prev_cart)):
            item = await get_data_by_id(int(prev_cart[i]))
            await message.answer_photo(item[6], caption=f'<b>Код товара</b>: {item[0]}\n' +
                                                        f'<b>Тип</b>: {item[1]}\n' + 
                                                        f'<b>Название</b>: {item[2]}\n' +
                                                        f'<b>Бренд</b>: {item[3]}\n' + 
                                                        f'<b>Описание</b>: {item[4]}\n' + 
                                                        f'<b>Цена</b>: {item[5]}', parse_mode='HTML',
                                                        reply_markup=keyboards.item_in_cart)
        await message.answer('Ваша корзина', reply_markup=keyboards.cart)

    
    
@catalog_router.callback_query(F.data == "обувь")
async def get_shoes(callback: Message):
    await callback.answer("Вы выбрали каталог 'Обувь'")
    data = await get_data_by_type("обувь")
    if data == []:
        await callback.message.answer("Пусто..")
    else:
        await callback.message.answer('Загружаю товар...')
        await asyncio.sleep(1)
        for item in range(len(data)):
            await asyncio.sleep(0.3)
            await callback.message.answer_photo(data[item][6], caption=f'<b>Код товара</b>: {data[item][0]}\n' +
                                                                        f'<b>Тип</b>: {data[item][1]}\n' + 
                                                                        f'<b>Название</b>: {data[item][2]}\n' +
                                                                        f'<b>Бренд</b>: {data[item][3]}\n' + 
                                                                        f'<b>Описание</b>: {data[item][4]}\n' +
                                                                        f'<b>Цена</b>: {data[item][5]}', parse_mode='HTML',
                                                                        reply_markup=keyboards.item)

    
@catalog_router.callback_query(F.data == "одежда")
async def get_clothes(callback: Message):
    await callback.answer("Вы выбрали каталог 'Одежда'")
    data = await get_data_by_type("одежда")
    if data == []:
        await callback.message.answer("Пусто..")
    else:
        await callback.message.answer('Загружаю товар...')
        await asyncio.sleep(1)
        for item in range(len(data)):
            await asyncio.sleep(0.3)
            await callback.message.answer_photo(data[item][6], caption=f'<b>Код товара</b>: {data[item][0]}\n' +
                                                                        f'<b>Тип</b>: {data[item][1]}\n' + 
                                                                        f'<b>Название</b>: {data[item][2]}\n' +
                                                                        f'<b>Бренд</b>: {data[item][3]}\n' + 
                                                                        f'<b>Описание</b>: {data[item][4]}\n' +
                                                                        f'<b>Цена</b>: {data[item][5]}', parse_mode='HTML',
                                                                        reply_markup=keyboards.item)
    
    
@catalog_router.callback_query(F.data == "головные уборы")
async def get_headdress(callback: Message):
    await callback.answer("Вы выбрали каталог 'Головные уборы'")
    data = await get_data_by_type("головные уборы")
    if data == []:
        await callback.message.answer("Пусто..")
    else:
        await callback.message.answer('Загружаю товар...')
        await asyncio.sleep(1)
        for item in range(len(data)):
            await asyncio.sleep(0.3)
            await callback.message.answer_photo(data[item][6], caption=f'<b>Код товара</b>: {data[item][0]}\n' +
                                                                        f'<b>Тип</b>: {data[item][1]}\n' + 
                                                                        f'<b>Название</b>: {data[item][2]}\n' +
                                                                        f'<b>Бренд</b>: {data[item][3]}\n' + 
                                                                        f'<b>Описание</b>: {data[item][4]}\n' +
                                                                        f'<b>Цена</b>: {data[item][5]}', parse_mode='HTML',
                                                                        reply_markup=keyboards.item)
            
            
async def get_id_by_caption(caption):
    index_start = caption.find(': ') + 2
    index_finish = caption.find('\n')
    id = caption[index_start:index_finish]
    return id

            
@catalog_router.callback_query(F.data == "to_cart")
async def add_item_to_cart(callback: CallbackQuery):
    i_id = await get_id_by_caption(callback.message.caption)
    data = await get_user_data_by_user_id(callback.from_user.id)
    prev_cart = data[4]
    
    if prev_cart is None:
        prev_cart = i_id
    elif i_id in prev_cart:
        await callback.answer("Такой товар уже есть в корзине!")
        return
    else:
        prev_cart += f', {i_id}'
        
    await add_item_to_cart_db(callback.from_user.id, prev_cart)
    await callback.answer("Товар добавлен в корзину!")
    
    
@catalog_router.callback_query(F.data == "from_cart")
async def del_item_from_cart(callback: CallbackQuery):
    i_id = await get_id_by_caption(callback.message.caption)
    data = await get_user_data_by_user_id(callback.from_user.id)
    cart = data[4].split(', ')
    cart.remove(i_id)
    
    if len(cart) == 0:
        cart = None
    else:
        cart = ', '.join(cart)
        
    await update_cart_id(callback.from_user.id, cart)
    await callback.message.delete()
    await callback.answer("Товар удален из корзину!")
    
