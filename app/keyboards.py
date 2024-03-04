from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Каталог")
        ],
        [
            KeyboardButton(text="Избранное"),
            KeyboardButton(text="Корзина")
        ],
        [
            KeyboardButton(text="Контакты")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)

start_admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Каталог")
        ],
        [
            KeyboardButton(text="Избранное"),
            KeyboardButton(text="Корзина")
        ],
        [
            KeyboardButton(text="Контакты")
        ],
        [
            KeyboardButton(text="Админ-панель")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)

admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить товар"),
            KeyboardButton(text="Удалить товар")
        ],
        [
            KeyboardButton(text="Изменить товар")
        ],
        [
            KeyboardButton(text="Сделать рассылку")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)


# INLINE KEYBOARDS

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Обувь", callback_data="обувь")
    ],
    [
        InlineKeyboardButton(text="Одежда", callback_data="одежда")
    ],
    [
        InlineKeyboardButton(text="Головные уборы", callback_data="головные уборы")
    ]
])

item = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Добавить в избранное", callback_data="to_favorite")
    ],
    [
        InlineKeyboardButton(text="Добавить в корзину", callback_data="to_cart")
    ]
])