from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

lang = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Uzb')],
        [KeyboardButton('Rus')],
        [KeyboardButton('Eng')],
    ],
    resize_keyboard=True
)
contact_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Ulashish', request_contact=True)]
    ],
    resize_keyboard=True
)

kop = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Xa", callback_data='Xa')],
        [InlineKeyboardButton("Yo'q", callback_data="Yo'q")],
        [InlineKeyboardButton("Orqaga", callback_data='Orqaga')],
    ]
)

contact_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Поделиться 📞', request_contact=True)]
    ],
    resize_keyboard=True
)
contact_eng = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Share', request_contact=True)]
    ],
    resize_keyboard=True
)

user_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Qarzdorlikni tekshirish')],
        [KeyboardButton("Seriya bo'yicha izlash")],
        [KeyboardButton('Biz bilan bog’lanish')],
        [KeyboardButton('Akt sverka olish')]
    ],
    resize_keyboard=True
)

user_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Проверка долга ＄')],
        [KeyboardButton('Связаться с нами 📞')],
        [KeyboardButton('Приобретение акта 🧾')]
    ],
    resize_keyboard=True
)

user_eng = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Debt check ＄')],
        [KeyboardButton('Contact us 📞')],
        [KeyboardButton('Acquiring an act 🧾')]
    ],
    resize_keyboard=True
)





akt_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('1', callback_data='1'),
         InlineKeyboardButton('2', callback_data='2'),
         InlineKeyboardButton('3', callback_data='3')]
    ]
)


























