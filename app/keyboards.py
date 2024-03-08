from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛄Каталог")
        ],
        [
            KeyboardButton(text="🛒Корзина")
        ],
        [
            KeyboardButton(text="👨‍💻Контакты")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)

start_admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛄Каталог")
        ],
        [
            KeyboardButton(text="🛒Корзина")
        ],
        [
            KeyboardButton(text="👨‍💻Контакты")
        ],
        [
            KeyboardButton(text="⚙️Админ-панель")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)

admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🆕Добавить товар"),
            KeyboardButton(text="🚫Удалить товар")
        ],
        [
            KeyboardButton(text="🔁Изменить товар")
        ],
        [
            KeyboardButton(text="🔉Сделать рассылку"),
            KeyboardButton(text="📊Статистика")
        ],
        [
            KeyboardButton(text="⬅️Назад"),
            KeyboardButton(text="🔄Сбросить")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие.'
)

cart = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📦Оформить заказ"),
        ],
        [
            KeyboardButton(text="⬅️Назад")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие.'
)


cancel_order = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚫Отменить заказ"),
        ],
        [
            KeyboardButton(text="🔁Оформить заново"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Оформление заказа...'
)


# INLINE KEYBOARDS

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="👟Обувь", callback_data="обувь")
    ],
    [
        InlineKeyboardButton(text="🎽Одежда", callback_data="одежда")
    ],
    [
        InlineKeyboardButton(text="🧢Головные уборы", callback_data="головные уборы")
    ]
])


subtype_shoes = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Спортивная обувь", callback_data="спорт обувь")
    ],
    [
        InlineKeyboardButton(text="Зимняя обувь", callback_data="зимняя обувь")
    ],
    [
        InlineKeyboardButton(text="Классическая обувь", callback_data="класс обувь")
    ],
    [
        InlineKeyboardButton(text="Не важно", callback_data="nomatter")
    ]
])

subtype_clothes = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Спортивная одежда", callback_data="спорт одежда")
    ],
    [
        InlineKeyboardButton(text="Куртки", callback_data="куртки")
    ],
    [
        InlineKeyboardButton(text="Брюки", callback_data="брюки")
    ],
    [
        InlineKeyboardButton(text="Рубашки", callback_data="рубашки")
    ],
    [
        InlineKeyboardButton(text="Футболки", callback_data="футболки")
    ],
    [
        InlineKeyboardButton(text="Не важно", callback_data="nomatter")
    ]
])

subtype_headdress = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Кепки", callback_data="кепки")
    ],
    [
        InlineKeyboardButton(text="Зимние шапки", callback_data="зимниешапки")
    ],
    [
        InlineKeyboardButton(text="Шляпы", callback_data="шляпы")
    ],
    [
        InlineKeyboardButton(text="Не важно", callback_data="nomatter")
    ]
])


item = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📌Добавить в корзину", callback_data="to_cart")
    ]
])

item_in_cart = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🚫Убрать из корзины", callback_data="from_cart")
    ]
])

confirm = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🆗Подтвердить", callback_data="confirm_order")
    ]
])