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
            KeyboardButton(text="⬅️Назад")
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