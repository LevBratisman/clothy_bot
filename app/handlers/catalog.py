from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.enums import ContentType
import json

import asyncio
import os

from app import keyboards
from app.database import get_data_by_type, get_user_data_by_user_id, add_item_to_cart_db, get_data_by_id, update_cart_id, get_item_by_type_subtype


catalog_router = Router()


class ItemFilter(StatesGroup):
    type = State()
    subtype = State()
    

@catalog_router.message((F.text == "🛄Каталог") | (F.text == "/catalog"))
async def catalog(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ItemFilter.type)
    await message.answer("Выберите категорию", reply_markup=keyboards.catalog)
    
    
@catalog_router.callback_query(ItemFilter.type)
async def get_subtypes(callback: CallbackQuery, state: FSMContext):
    await state.update_data(type=callback.data)
    if callback.data == "обувь":
        await state.set_state(ItemFilter.subtype)
        await callback.message.edit_text("Теперь выберите подтип товара", 
                                      reply_markup=keyboards.subtype_shoes)
    elif callback.data == "одежда":
        await state.set_state(ItemFilter.subtype)
        await callback.message.edit_text("Теперь выберите подтип товара", 
                                      reply_markup=keyboards.subtype_clothes)
    elif callback.data == "головные уборы":
        await state.set_state(ItemFilter.subtype)
        await callback.message.edit_text("Теперь выберите подтип товара", 
                                      reply_markup=keyboards.subtype_headdress)
        
        
@catalog_router.callback_query(ItemFilter.subtype)
async def add_item_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(subtype=callback.data)
    data = await state.get_data()
    if data["type"] == "обувь":
        await get_shoes(callback, state)
    elif data["type"] == "одежда":
        await get_clothes(callback, state)
    elif data["type"] == "головные уборы":
        await get_headdress(callback, state)
        


@catalog_router.message(F.text == "⬅️Назад")
async def back_to_manu(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Меню", reply_markup=keyboards.start_admin_keyboard)
    else:
        await message.answer("Меню", reply_markup=keyboards.start_keyboard)
    

    
@catalog_router.message(F.text == "🛒Корзина")
async def basket(message: Message):
    data = await get_user_data_by_user_id(message.from_user.id)
    prev_cart = data[4]
    if prev_cart is None:
        await message.answer("Корзина пуста")
    else:
        prev_cart = prev_cart.split(', ')
        for i in range(len(prev_cart)):
            item = await get_data_by_id(int(prev_cart[i]))
            print(item)
            await message.answer_photo(item[7], caption=f'<b>#️⃣Код товара</b>: {item[0]}\n' +
                                                                        f'<b>🏷Тип</b>: {item[1]}\n' + 
                                                                        f'<b>🔧Подтип</b>: {item[2]}\n' + 
                                                                        f'<b>🔤Название</b>: {item[3]}\n' +
                                                                        f'<b>🌐Бренд</b>: {item[4]}\n' + 
                                                                        f'<b>📝Описание</b>: {item[5]}\n' +
                                                                        f'<b>💰Цена</b>: {item[6]}', parse_mode='HTML',
                                                        reply_markup=keyboards.item_in_cart)
        await message.answer('Теперь вы можете оформить заказ', reply_markup=keyboards.cart)

    
    
@catalog_router.callback_query(F.data == "обувь")
async def get_shoes(callback: Message, state: FSMContext):
    await callback.answer("Вы выбрали каталог 'Обувь'")
    filter_data = await state.get_data()
    if filter_data["subtype"] == "nomatter":
        data = await get_data_by_type(filter_data["type"])
    else:
        data = await get_item_by_type_subtype(filter_data["type"], filter_data["subtype"])
        
    if data == []:
        await callback.message.answer("Пусто..")
    else:
        await callback.message.edit_text('Обувь')
        await callback.message.answer('Загружаю товар...')
        await asyncio.sleep(1)
        for item in range(len(data)):
            await asyncio.sleep(0.3)
            await callback.message.answer_photo(data[item][7], caption=f'<b>#️⃣Код товара</b>: {data[item][0]}\n' +
                                                                        f'<b>🏷Тип</b>: {data[item][1]}\n' + 
                                                                        f'<b>🔧Подтип</b>: {data[item][2]}\n' + 
                                                                        f'<b>🔤Название</b>: {data[item][3]}\n' +
                                                                        f'<b>🌐Бренд</b>: {data[item][4]}\n' + 
                                                                        f'<b>📝Описание</b>: {data[item][5]}\n' +
                                                                        f'<b>💰Цена</b>: {data[item][6]}', parse_mode='HTML',
                                                                        reply_markup=keyboards.item)
        await state.clear()

    
@catalog_router.callback_query(F.data == "одежда")
async def get_clothes(callback: Message, state: FSMContext):
    await callback.answer("Вы выбрали каталог 'Одежда'")
    filter_data = await state.get_data()
    if filter_data["subtype"] == "nomatter":
        data = await get_data_by_type(filter_data["type"])
    else:
        data = await get_item_by_type_subtype(filter_data["type"], filter_data["subtype"])
        
    if data == []:
        await callback.message.answer("Пусто..")
    else:
        await callback.message.edit_text('Одежда')
        await callback.message.answer('Загружаю товар...')
        await asyncio.sleep(1)
        for item in range(len(data)):
            await asyncio.sleep(0.3)
            await callback.message.answer_photo(data[item][7], caption=f'<b>#️⃣Код товара</b>: {data[item][0]}\n' +
                                                                        f'<b>🏷Тип</b>: {data[item][1]}\n' + 
                                                                        f'<b>🔧Подтип</b>: {data[item][2]}\n' + 
                                                                        f'<b>🔤Название</b>: {data[item][3]}\n' +
                                                                        f'<b>🌐Бренд</b>: {data[item][4]}\n' + 
                                                                        f'<b>📝Описание</b>: {data[item][5]}\n' +
                                                                        f'<b>💰Цена</b>: {data[item][6]}', parse_mode='HTML',
                                                                        reply_markup=keyboards.item)
        await state.clear()
        
    
    
@catalog_router.callback_query(F.data == "головные уборы")
async def get_headdress(callback: Message, state: FSMContext):
    await callback.answer("Вы выбрали каталог 'Головные уборы'")
    filter_data = await state.get_data()
    if filter_data["subtype"] == "nomatter":
        data = await get_data_by_type(filter_data["type"])
    else:
        data = await get_item_by_type_subtype(filter_data["type"], filter_data["subtype"])
        
    if data == []:
        await callback.message.answer("Пусто..")
    else:
        await callback.message.edit_text('Головные уборы')
        await callback.message.answer('Загружаю товар...')
        await asyncio.sleep(1)
        for item in range(len(data)):
            await asyncio.sleep(0.3)
            await callback.message.answer_photo(data[item][7], caption=f'<b>#️⃣Код товара</b>: {data[item][0]}\n' +
                                                                        f'<b>🏷Тип</b>: {data[item][1]}\n' + 
                                                                        f'<b>🔧Подтип</b>: {data[item][2]}\n' + 
                                                                        f'<b>🔤Название</b>: {data[item][3]}\n' +
                                                                        f'<b>🌐Бренд</b>: {data[item][4]}\n' + 
                                                                        f'<b>📝Описание</b>: {data[item][5]}\n' +
                                                                        f'<b>💰Цена</b>: {data[item][6]}', parse_mode='HTML',
                                                                        reply_markup=keyboards.item)
        await state.clear()
            
            
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
        await update_cart_id(callback.from_user.id, cart)
        await callback.message.delete()
        await callback.answer("Товар удален из корзины!")
        if callback.from_user.id == int(os.getenv('ADMIN_ID')):
            await callback.message.answer("Корзина пуста", reply_markup=keyboards.start_admin_keyboard)
        else:
            await callback.message.answer("Корзина пуста" , reply_markup=keyboards.start_keyboard)
    else:
        cart = ', '.join(cart)
        await update_cart_id(callback.from_user.id, cart)
        await callback.message.delete()
        await callback.answer("Товар удален из корзины!")
    
