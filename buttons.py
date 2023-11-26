from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

lang = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('🇺🇿')],
        [KeyboardButton('🇷🇺')],
        [KeyboardButton('🇬🇧')],
    ],
    resize_keyboard=True
)
contact_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Ulashish 📞', request_contact=True)]
    ],
    resize_keyboard=True
)

contact_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Поделиться 📞', request_contact=True)]
    ],
    resize_keyboard=True
)
contact_eng = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Share 📞', request_contact=True)]
    ],
    resize_keyboard=True
)

user_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Qarzdorlikni tekshirish ＄')],
        [KeyboardButton('Biz bilan bog’lanish 📞')],
        [KeyboardButton('Akt sverka olish 🧾')]
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

c_button_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('AllSumm'),
        #  KeyboardButton('Currency'),
        #  KeyboardButton('Contract'),
        #  KeyboardButton('ContractSumm'),
        #  KeyboardButton('ContractCurrency'),
        #  KeyboardButton('ContractEkvivalent'),
         KeyboardButton('Bosh menyuga qaytish 🔙')]
    ],
    resize_keyboard=True,
)

c_button_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('AllSumm'),
        #  KeyboardButton('Currency'),
        #  KeyboardButton('Contract'),
        #  KeyboardButton('ContractSumm'),
        #  KeyboardButton('ContractCurrency'),
        #  KeyboardButton('ContractEkvivalent'),
         KeyboardButton('Вернуться в главное меню 🔙')]
    ],
    resize_keyboard=True,
)

c_button_eng = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('AllSumm'),
        #  KeyboardButton('Currency'),
        #  KeyboardButton('Contract'),
        #  KeyboardButton('ContractSumm'),
        #  KeyboardButton('ContractCurrency'),
        #  KeyboardButton('ContractEkvivalent'),
         KeyboardButton('Return to main menu 🔙')]
    ],
    resize_keyboard=True,
)

akt_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('1', callback_data='1'),
         InlineKeyboardButton('2', callback_data='2'),
         InlineKeyboardButton('3', callback_data='3')]
    ]
)


























