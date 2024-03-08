from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ShippingQuery
from aiogram.filters import CommandStart
from aiogram.enums import ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from app import keyboards
from app.database import get_user_data_by_user_id, get_data_by_id, add_order_db

load_dotenv(find_dotenv())

cart_router = Router()


class NewOrder(StatesGroup):
    user_id = State()
    order = State()
    total_cost = State()
    full_name = State()
    adress = State()
    phone = State()
    email = State()
    
    
    
@cart_router.message(F.text == "🚫Отменить заказ")
async def cancel_order(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Меню", reply_markup=keyboards.start_admin_keyboard)
    else:
        await message.answer("Меню", reply_markup=keyboards.start_keyboard)
        
        
@cart_router.message(F.text == "🔁Оформить заново")
async def reset_order(message: Message, state: FSMContext):
    await state.clear()
    await cart(message, state)


@cart_router.message(F.text == "📦Оформить заказ")
async def cart(message: Message, state: FSMContext):
    await message.answer("▫️Ваш заказ:", reply_markup=keyboards.cancel_order)
    data = await get_user_data_by_user_id(message.from_user.id)
    cart = data[4]
    order = []
    total_cost = 0
    if cart is None:
        await message.answer("Корзина пуста")
    else:
        await state.set_state(NewOrder.order)
        cart = cart.split(', ')
        for i in range(len(cart)):
            item = await get_data_by_id(int(cart[i]))
            total_cost += int(item[6])
            order.append(str(item[0]))
            await message.answer(f'{i + 1}. <b>Название</b>: {item[3]}\n' +
                                 f'    <b>Цена</b>: {item[6]}', parse_mode='HTML')
        order = ', '.join(order)
        await message.answer(f'<b>💰Итого</b>: {total_cost} ₽\n' +
                             f'----------------\n', parse_mode='HTML')
        
        await state.update_data(user_id=data[0])
        await state.update_data(order=order)
        await state.update_data(total_cost=total_cost)
        await asyncio.sleep(1)
        await state.set_state(NewOrder.full_name)
        await message.answer("Теперь введите ФИО")
        
        

@cart_router.message(NewOrder.full_name)
async def set_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(NewOrder.adress)
    await message.answer("Теперь введите адрес доставки")
    
    
@cart_router.message(NewOrder.adress)
async def set_full_name(message: Message, state: FSMContext):
    await state.update_data(adress=message.text)
    await state.set_state(NewOrder.phone)
    await message.answer("Теперь введите номер телефона")
    
    
@cart_router.message(NewOrder.phone)
async def set_full_name(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(NewOrder.email)
    await message.answer("Последний шаг! введите email")
    
    
@cart_router.message(NewOrder.email)
async def set_full_name(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await message.answer("🔸Информация о заказе:")
    await message.answer(f'<b>ФИО:</b> {data["full_name"]}\n' +
                         f'<b>Адрес доставки:</b> {data["adress"]}\n' +
                         f'<b>Телефон:</b> {data["phone"]}\n' +
                         f'<b>Email:</b> {data["email"]}\n' +
                         f'<b>Товары(код товара):</b> {data["order"]}\n' +
                         f'<b>Итого:</b> {data["total_cost"]} ₽\n' +
                         f'----------------\n', parse_mode='HTML')
    await message.answer("Подтвердите заказ", reply_markup=keyboards.confirm)

    
    
@cart_router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await callback.message.delete()
    print(data)
    await add_order_db(data)
    PRICE = LabeledPrice(label='Товары', amount=data["total_cost"] * 100)
    TOKEN = os.getenv('PAYMENTS_TOKEN')
    #await add_order_db(data)
    await bot.send_invoice(
                            callback.from_user.id,
                            title='Платеж',
                            description='Тестовый платеж',
                            provider_token=TOKEN,
                            currency='rub',
                            photo_url='https://runamagik.ru/wp-content/uploads/2023/12/JxUtcBpNOfM.jpg',
                            photo_height=1280,  # !=0/None, иначе изображение не покажется
                            photo_width=1026,
                            photo_size=1000,
                            is_flexible=False,  # True если конечная цена зависит от способа доставки
                            prices=[PRICE],
                            start_parameter='time-machine-example',
                            payload='some-invoice-payload-for-our-internal-use',
                            request_timeout=60
    )
    await state.clear()
    if callback.from_user.id == int(os.getenv('ADMIN_ID')):
        await callback.message.answer_sticker('CAACAgIAAx0Cd9gAAe8AAypl6eHRwL3TUQhDivk2zOnK4Zqz-wACHAEAAjDUnRFu6owpqq4XTjQE')
        await asyncio.sleep(1)
        await callback.message.answer(f'Заказ оформлен! Товар уже в пути\n' +
                                  f'‼️В данном боте используется тестовая система платежей. Она не работает!',
                                  reply_markup=keyboards.start_admin_keyboard, show_alert=True)
    else:
        await callback.message.answer(f'Заказ оформлен!\n' +
                                  f'‼️В данном боте используется тестовая система платежей. Она не работает!',
                                  reply_markup=keyboards.start_keyboard, show_alert=True)
    
    
    
@cart_router.shipping_query(F.shipping_query)
async def shipping(shipping_query: ShippingQuery):
    await shipping_query.answer(ok=True)
    print("SHIPPING: ")
    print(shipping_query)
    
    
@cart_router.message(F.pre_checkout_query)
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    print("Подтверждение оплаты")
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    print(pre_checkout_query)
    
    
@cart_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    print("SUCCESSFUL PAYMENT!")