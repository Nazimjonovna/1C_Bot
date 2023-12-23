import logging
import asyncio
import datetime
from aiogram import Bot, Dispatcher, executor, types
from buttons import *
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import re
import io
import requests
import os
from aiogram.types import CallbackQuery
from dotenv import load_dotenv
load_dotenv()
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Your API endpoint URL
api_url = 'http://5.182.26.180:55565/telegram/hs/hl/gd'
login = 'HILOL'
password = '0ut0fb0unD'

# Token of tg_Bot
# API_TOKEN = '6619844226:AAFUabaziFZyL70r3dmcF1eHBU66dA1y4Fo'
API_TOKEN = '5666343720:AAEKYBzyoDlx3OJX8xQQOAQwpIqDNk6ETbw'

headers = {
            'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }


# Configure logging
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

class TimeInput(StatesGroup):
    start_time = State()
    end_time = State()

class Input(StatesGroup):
    sery = State()
    end_time = State()
    contracts = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Tilni tanlang\n\nВыберите язык\n\nSelect language", reply_markup=lang)


@dp.message_handler(text = "🇺🇿")
async def uzb(message: types.Message):
    global lan
    lan = message.text
    params = {
        'type':"comment"
    }
    try:
        response = requests.get(api_url, params=params, headers=headers)
        if response.ok:
            if 'application/json' in response.headers.get('Content-Type', ''):
                data = response.json()
                result = response.text
            else:
                result = f"Response is not in JSON format: {response.text}"
        else:
            result = f"Request failed with status code {response.status_code}: {response.reason}"
        await message.answer(f"{data.get('UZ')}"+"\nIdentifikatsiyadan o’tish uchun telefon raqamingizni ulashing.", reply_markup=contact_uz)

    except requests.exceptions.RequestException as e:
        result = f"Request failed: {e}"
        await message.answer(f"sizdagi xatolik{result}")




    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def uzb_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = message.contact.phone_number
        chat_id =  message.from_user.id
        params = {
            'type': 'phone',
            'chat_id': chat_id,
            'phone_number': phone_number,
            'language':lan
        }
        try:
            response = requests.get(api_url, params=params, headers=headers)
            if response.ok:
                if 'application/json' in response.headers.get('Content-Type', ''):
                    data = response.json()
                    p = data.get("UZ")
                    result = response.text
                    await message.answer(f"{p}", reply_markup=user_uz)
                else:
                    result = f"Response is not in JSON format: {response.text}"
            else:
                result = f"Request failed with status code {response.status_code}: {response.reason}"
            # await message.answer(f"{data.get('UZ')}", reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            result = f"Request failed: {e}"
            await message.answer(f"{data.get('UZ')}")

    @dp.message_handler(text="Qarzdorlikni tekshirish")
    async def tel1(message: types.Message):
        params = {
            "type": "contracts",
            "chat_id": message.from_user.id
        }
        response = requests.get(api_url, params=params, headers=headers)
        global ta
        ta = {}
        if response:
            data = response.json()
            if data is not None and 'contracts' in data and data['contracts']:
                buttons = []
                row = []
                for index, contract_info in enumerate(data['contracts'], start=1):
                    button_text = str(contract_info['contract'])
                    ta[str(contract_info['contract'])] = str(contract_info['contractID'])
                    button = KeyboardButton(text=button_text)
                    row.append(button)
                    if index % 2 == 0:
                        buttons.append([button])
                        row = []
                if row:
                    buttons.append(row)
                back_button = KeyboardButton(text="Orqaga")
                buttons.append([back_button])
                reply_markup = ReplyKeyboardMarkup(keyboard=buttons)
                await message.answer("Choose which one of them", reply_markup=reply_markup)
                await Input.contracts.set()
            else:
                await message.answer("data yoq sizda", reply_markup=user_uz)
        else:
            await message.answer("Quyidagilardan tanlang: ", reply_markup=user_uz)

        @dp.message_handler(state=Input.contracts)
        async def tel2(message: types.Message, state: FSMContext):
            messa = message.text
            if messa != "Orqaga":
                params = {
                    "type": "debt",
                    "chat_id": message.from_user.id
                }
                response = requests.get(api_url, params=params, headers=headers)
                if response:
                    data = response.json()
                    global summ, contract_id
                    contract = message.text
                    contract_id = ta[contract]
                    summ = data['allsumm']
                    val = data['currency']
                    for i in range(len(data['contracts'])):
                        if data['contracts'][i]['contract'] == contract:
                            contractsumm = data['contracts'][i]['contractsumm']
                            contractcurrency = data['contracts'][i]['contractcurrency']
                            contractekvivalent = data['contracts'][i]['contractekvivalent']
                    await message.answer(
                        f"Sizning jammi qarzdorligingiz: {summ} {val},\n va ushbu {contract}-shartnomasi bo'yicha ma'lumotlar:\n{contractsumm} {contractcurrency}\n ekvvivaletligi: {contractekvivalent}")
                    await state.finish()
                    await message.answer("Quyidagilardan tanlang: ", reply_markup=kop)
            else:
                await message.answer('Orqaga', reply_markup=user_uz)

                @dp.callback_query_handler(text='Xa')
                async def tel3(callback_query: types.CallbackQuery):
                    user_id = callback_query.from_user.id
                    date = str(datetime.datetime.today().date()) + "T00:00:00"
                    params = {
                        "type": "debt_check",
                        "chat_id": message.from_user.id,
                        "contract_id": contract_id,
                        "check": "true",
                        'summ': summ,
                        'date': date
                    }
                    response = requests.get(api_url, params=params, headers=headers)
                    if response:
                        data = response.json()
                        await bot.send_message(user_id, f"{data['succed_text']}", reply_markup = user_uz)

                @dp.callback_query_handler(text="Yo'q")
                async def tel4(callback_query: types.CallbackQuery):
                    user_id = callback_query.from_user.id
                    date = str(datetime.datetime.today().date()) + "T00:00:00"
                    params = {
                        "type": "debt_check",
                        "chat_id": message.from_user.id,
                        "contract_id": contract_id,
                        "check": "true",
                        'summ': summ,
                        'date': date
                    }
                    response = requests.get(api_url, params=params, headers=headers)
                    if response:
                        await bot.send_message(user_id, f"{data['succed_text']}", reply_markup = user_uz)

                @dp.callback_query_handler(text="Orqaga")
                async def tel4(callback_query: types.CallbackQuery):
                    chat_id = callback_query.from_user.id
                    await bot.answer_callback_query(callback_query.id)
                    await bot.edit_message_reply_markup(chat_id=chat_id,
                                                        message_id=callback_query.message.message_id,
                                                        reply_markup=None)

    @dp.message_handler(text="Seriya bo'yicha izlash")
    async def tel4(message: types.Message):
        await message.answer("Seriya raqamini kiriting:")
        await Input.sery.set()

    @dp.message_handler(state=Input.sery)
    async def act(message: types.Message, state: FSMContext):
        global sery
        sery = message.text
        params = {
            "type": "search_by_series",
            "sery": 353742533112405,
            "chat_id": message.from_user.id
        }
        response = requests.get(api_url, params=params, headers=headers)
        if response:
            data = response.json()
            contragent = data['contragent']
            number = data['number']
            nomenclature = data['nomenclature']
            await message.answer(f"contragent: {contragent}\nNomer: {number}\nNomenclature: {nomenclature}")
            await state.finish()

    @dp.message_handler(text = 'Biz bilan bog’lanish')
    async def admin(message: types.Message):
        await message.answer("Admin: @pm_hilol")

        @dp.message_handler(text='Akt sverka olish') # qayta qayta bossa bo'lishi kk forga o'xshab
        async def start_handler(message: types.Message, state: FSMContext):
            params = {
                "type": "contracts",
                "chat_id": message.from_user.id
            }
            response = requests.get(api_url, params=params, headers=headers)
            global ta, calback
            ta =[]
            calback = []
            data = response.json()
            print("ctla", data['contracts'])
            buttons = []
            for contract_info in data['contracts']:
                button_text = str(contract_info['contract'])
                cal_back = str(contract_info['contractID'])
                ta.append(str(contract_info['contract']))
                calback.append(str(contract_info['contractID']))
                button = InlineKeyboardButton(text=button_text, callback_data=cal_back)
                buttons.append([button])
            hammasi = InlineKeyboardButton(text="Hammasi", callback_data="Hammasi")
            orqaga = InlineKeyboardButton(text="Orqaga", callback_data="Orqaga")
            buttons.append([hammasi])
            ta.append('Hammasi')
            calback.append('Hammasi')
            buttons.append([orqaga])
            ta.append('Orqaga')
            calback.append('Orqaga')

            reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
            await message.answer("Shartnomalar", reply_markup=reply_markup)
            await state.set_state("waiting_for_contract")

        @dp.callback_query_handler(state = 'waiting_for_contract') # ishlasi kk to'xtivsz
        async def act(callback_query: CallbackQuery, state: FSMContext):
            global msgcall
            msgcall = callback_query.data
            print(msgcall)
            if msgcall != "Orqaga":
                await state.finish()
                await TimeInput.start_time.set()
                await callback_query.message.answer("Boshlang'ich sanani kiriting(masalan: Yil-OY-Kun): ")
            elif msgcall == "Hammasi":
                await state.finish()
                await TimeInput.start_time.set()
                await callback_query.message.answer("Boshlang'ich sanani kiriting(masalan: Yil-OY-Kun): ")
            else:
                await callback_query.message.edit_reply_markup(reply_markup=None)


        @dp.message_handler(state=TimeInput.start_time)
        async def start_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['start'] = message.text
                    global start_t
                    start_t = message.text
                    await TimeInput.next()
                    await message.answer("Tugash sanani kiriting(masalan: Yil-OY-Kun): ")
            else:
                await message.answer("To'g'ri formatda sanani kiriting(masalan: Yil-OY-Kun): ")


        @dp.message_handler(state=TimeInput.end_time)
        async def end_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['finish'] = message.text
                    global start_t
                    start = start_t + 'T00:00:00'
                    finish = message.text + 'T00:00:00'
                    chat_id = message.from_user.id
                    if msgcall == 'Hammasi':
                        if start_t < message.text:
                            params = {
                                "type": "reconciliation_act",
                                "chat_id": chat_id,
                                "start": start,
                                "finish": finish
                            }
                    if start_t < message.text:
                        params = {
                            "type": "reconciliation_act",
                                "chat_id": chat_id,
                                "start":start,
                                "finish":finish,
                                'contract_id':msgcall
                        }
                        print('params', params)
                        response = requests.get(api_url, params=params, headers=headers)
                        try:
                            if response.ok:
                                content_type = response.headers.get('Content-Type', '')
                                if 'application/json' in content_type:
                                    data = response.json()
                                    if data.get('allsumm') is None:
                                        await message.answer("Sizda hozircha mablag' yo ")
                                    else:
                                        await message.answer(f"{data['allsumm']}----{data['contracts']}")
                                    await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                                elif 'application/octet-stream' in content_type or 'application/vnd.ms-excel' in content_type:
                                    bio = io.BytesIO(response.content)
                                    bio.name = 'received_file.xlsx'
                                    await message.answer_document(document=bio)
                                else:
                                    result = f"Unknown Content-Type: {content_type}"
                                    await message.answer(f"Sizdagi xatolik {result}")
                            else:
                                result = f"Request failed with status code {response.status_code}: {response.reason}"
                                # print("error", result)
                                await message.answer(f"Sizdagi xatolik {result}")

                        except requests.exceptions.RequestException as e:
                            result = f"Request failed: {e}"
                            await message.answer(f"Sizdagi xatolik exepdan {result}")
                        await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                        await state.finish()
                    else:
                        await message.answer("Boshlanish sanasi Tugash sanasidan  katta!")
                        await TimeInput.start_time.set()
                        await message.answer("Boshlang'ich sanani kiriting(masalan: Yil-OY-Kun): ")



































@dp.message_handler(text = "🇷🇺")
async def uzb(message: types.Message):
    global lan
    lan = message.text
    params = {
        'type':"comment"
    }
    try:
        response = requests.get(api_url, params=params, headers=headers)
        if response.ok:
            if 'application/json' in response.headers.get('Content-Type', ''):
                data = response.json()
                result = response.text
            else:
                result = f"Response is not in JSON format: {response.text}"
        else:
            result = f"Request failed with status code {response.status_code}: {response.reason}"
        await message.answer(f"{data.get('RU')}"+"\nПоделитесь своим номером телефона для аутентификации.", reply_markup=contact_ru)

    except requests.exceptions.RequestException as e:
        result = f"Request failed: {e}"
        await message.answer(f"sizdagi xatolik{result}")




    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def uzb_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = message.contact.phone_number
        chat_id =  message.from_user.id
        params = {
            'type': 'phone',
            'chat_id': chat_id,
            'phone_number': phone_number,
            'language':lan
        }
        try:
            response = requests.get(api_url, params=params, headers=headers)
            if response.ok:
                if 'application/json' in response.headers.get('Content-Type', ''):
                    data = response.json()
                    p = data.get("RU")
                    result = response.text
                    await message.answer(f"{p}", reply_markup=user_ru)
                else:
                    result = f"Response is not in JSON format: {response.text}"
            else:
                result = f"Request failed with status code {response.status_code}: {response.reason}"
            # await message.answer(f"{data.get('UZ')}", reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            result = f"Request failed: {e}"
            await message.answer(f"{data.get('RU')}")

    @dp.message_handler(text="Проверка долга ＄")
    async def tel1(message: types.Message):
        params = {
            "type": "contracts",
            "chat_id": message.from_user.id
        }
        response = requests.get(api_url, params=params, headers=headers)
        global ta
        ta = {}
        if response:
            data = response.json()
            if data is not None and 'contracts' in data and data['contracts']:
                buttons = []
                row = []
                for index, contract_info in enumerate(data['contracts'], start=1):
                    button_text = str(contract_info['contract'])
                    ta[str(contract_info['contract'])] = str(contract_info['contractID'])
                    button = KeyboardButton(text=button_text)
                    row.append(button)
                    if index % 2 == 0:
                        buttons.append([button])
                        row = []
                if row:
                    buttons.append(row)
                back_button = KeyboardButton(text="Назад")
                buttons.append([back_button])
                reply_markup = ReplyKeyboardMarkup(keyboard=buttons)
                await message.answer("Choose which one of them", reply_markup=reply_markup)
                await Input.contracts.set()
            else:
                await message.answer("у вас есть данные", reply_markup=user_ru)
        else:
            await message.answer("Выберите из следующих: ", reply_markup=user_ru)

        @dp.message_handler(state=Input.contracts)
        async def tel2(message: types.Message, state: FSMContext):
            messa = message.text
            if messa != "Назад":
                params = {
                    "type": "debt",
                    "chat_id": message.from_user.id
                }
                response = requests.get(api_url, params=params, headers=headers)
                if response:
                    data = response.json()
                    global summ, contract_id
                    contract = message.text
                    contract_id = ta[contract]
                    summ = data['allsumm']
                    val = data['currency']
                    for i in range(len(data['contracts'])):
                        if data['contracts'][i]['contract'] == contract:
                            contractsumm = data['contracts'][i]['contractsumm']
                            contractcurrency = data['contracts'][i]['contractcurrency']
                            contractekvivalent = data['contracts'][i]['contractekvivalent']
                    await message.answer(
                        f"Ваш общий долг: {summ} {val},\n и это {contract}-информация о контракте:\n{contractsumm} {contractcurrency}\n эквивалентность: {contractekvivalent}")
                    await state.finish()
                    await message.answer("Выберите из следующих: ", reply_markup=kop_ru)
            else:
                await message.answer('Назад', reply_markup=user_uz)

                @dp.callback_query_handler(text='Да')
                async def tel3(callback_query: types.CallbackQuery):
                    user_id = callback_query.from_user.id
                    date = str(datetime.datetime.today().date()) + "T00:00:00"
                    params = {
                        "type": "debt_check",
                        "chat_id": message.from_user.id,
                        "contract_id": contract_id,
                        "check": "true",
                        'summ': summ,
                        'date': date
                    }
                    response = requests.get(api_url, params=params, headers=headers)
                    if response:
                        data = response.json()
                        await bot.send_message(user_id, f"{data['succed_text']}", reply_markup = user_ru)

                @dp.callback_query_handler(text="Нет")
                async def tel4(callback_query: types.CallbackQuery):
                    user_id = callback_query.from_user.id
                    date = str(datetime.datetime.today().date()) + "T00:00:00"
                    params = {
                        "type": "debt_check",
                        "chat_id": message.from_user.id,
                        "contract_id": contract_id,
                        "check": "true",
                        'summ': summ,
                        'date': date
                    }
                    response = requests.get(api_url, params=params, headers=headers)
                    if response:
                        await bot.send_message(user_id, f"{data['succed_text']}", reply_markup = user_ru)

                @dp.callback_query_handler(text="Назад")
                async def tel4(callback_query: types.CallbackQuery):
                    chat_id = callback_query.from_user.id
                    await bot.answer_callback_query(callback_query.id)
                    await bot.edit_message_reply_markup(chat_id=chat_id,
                                                        message_id=callback_query.message.message_id,
                                                        reply_markup=None)

    @dp.message_handler(text="Поиск по серии")
    async def tel4(message: types.Message):
        await message.answer("Введите серийный номер:")
        await Input.sery.set()

    @dp.message_handler(state=Input.sery)
    async def act(message: types.Message, state: FSMContext):
        global sery
        sery = message.text
        params = {
            "type": "search_by_series",
            "sery": sery,
            "chat_id": message.from_user.id
        }
        response = requests.get(api_url, params=params, headers=headers)
        if response:
            data = response.json()
            contragent = data['contragent']
            number = data['number']
            nomenclature = data['nomenclature']
            await message.answer(f"contragent: {contragent}\nNomer: {number}\nNomenclature: {nomenclature}")
            await state.finish()

    @dp.message_handler(text = 'Связаться с нами 📞')
    async def admin(message: types.Message):
        await message.answer("Admin: @pm_hilol")

        @dp.message_handler(text='Приобретение акта 🧾') # qayta qayta bossa bo'lishi kk forga o'xshab
        async def start_handler(message: types.Message, state: FSMContext):
            params = {
                "type": "contracts",
                "chat_id": message.from_user.id
            }
            response = requests.get(api_url, params=params, headers=headers)
            global ta, calback
            ta =[]
            calback = []
            data = response.json()
            print("ctla", data['contracts'])
            buttons = []
            for contract_info in data['contracts']:
                button_text = str(contract_info['contract'])
                cal_back = str(contract_info['contractID'])
                ta.append(str(contract_info['contract']))
                calback.append(str(contract_info['contractID']))
                button = InlineKeyboardButton(text=button_text, callback_data=cal_back)
                buttons.append([button])
            hammasi = InlineKeyboardButton(text="Все", callback_data="Все")
            orqaga = InlineKeyboardButton(text="Назад", callback_data="Назад")
            buttons.append([hammasi])
            ta.append('Все')
            calback.append('Все')
            buttons.append([orqaga])
            ta.append('Назад')
            calback.append('Назад')

            reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
            await message.answer("Соглашения", reply_markup=reply_markup)
            await state.set_state("waiting_for_contract")

        @dp.callback_query_handler(state = 'waiting_for_contract')
        async def act(callback_query: CallbackQuery, state: FSMContext):
            global msgcall
            msgcall = callback_query.data
            print(msgcall)
            if msgcall != "Назад":
                await state.finish()
                await TimeInput.start_time.set()
                await callback_query.message.answer("Введите дату начала (например: ГГГГ-ММ-ДД): ")
            elif msgcall == "Все":
                await state.finish()
                await TimeInput.start_time.set()
                await callback_query.message.answer("BВведите дату начала (например: ГГГГ-ММ-ДД) ")
            else:
                await callback_query.message.edit_reply_markup(reply_markup=None)


        @dp.message_handler(state=TimeInput.start_time)
        async def start_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['start'] = message.text
                    global start_t
                    start_t = message.text
                    await TimeInput.next()
                    await message.answer("Введите дату окончания (например: ГГГГ-ММ-ДД): ")
            else:
                await message.answer("Введите дату в правильном формате (например: Год-Месяц-День): ")


        @dp.message_handler(state=TimeInput.end_time)
        async def end_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['finish'] = message.text
                    global start_t
                    start = start_t + 'T00:00:00'
                    finish = message.text + 'T00:00:00'
                    chat_id = message.from_user.id
                    if msgcall == 'Все':
                        if start_t < message.text:
                            params = {
                                "type": "reconciliation_act",
                                "chat_id": chat_id,
                                "start": start,
                                "finish": finish
                            }
                    if start_t < message.text:
                        params = {
                            "type": "reconciliation_act",
                                "chat_id": chat_id,
                                "start":start,
                                "finish":finish,
                                'contract_id':msgcall
                        }
                        response = requests.get(api_url, params=params, headers=headers)
                        try:
                            if response.ok:
                                content_type = response.headers.get('Content-Type', '')
                                if 'application/json' in content_type:
                                    data = response.json()
                                    if data.get('allsumm') is None:
                                        await message.answer("У вас еще нет средств")
                                    else:
                                        await message.answer(f"{data['allsumm']}----{data['contracts']}")
                                    await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                                elif 'application/octet-stream' in content_type or 'application/vnd.ms-excel' in content_type:
                                    bio = io.BytesIO(response.content)
                                    bio.name = 'received_file.xlsx'
                                    await message.answer_document(document=bio)
                                else:
                                    result = f"Unknown Content-Type: {content_type}"
                                    await message.answer(f"Sizdagi xatolik {result}")
                            else:
                                result = f"Request failed with status code {response.status_code}: {response.reason}"
                                # print("error", result)
                                await message.answer(f"Sizdagi xatolik {result}")

                        except requests.exceptions.RequestException as e:
                            result = f"Request failed: {e}"
                            await message.answer(f"Sizdagi xatolik exepdan {result}")
                        await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                        await state.finish()
                    else:
                        await message.answer("Дата начала больше даты окончания!")
                        await TimeInput.start_time.set()
                        await message.answer("Введите дату начала (например: ГГГГ-ММ-ДД):")













































@dp.message_handler(text = "🇺🇸")
async def uzb(message: types.Message):
    global lan
    lan = message.text
    params = {
        'type':"comment"
    }
    try:
        response = requests.get(api_url, params=params, headers=headers)
        if response.ok:
            if 'application/json' in response.headers.get('Content-Type', ''):
                data = response.json()
                result = response.text
            else:
                result = f"Response is not in JSON format: {response.text}"
        else:
            result = f"Request failed with status code {response.status_code}: {response.reason}"
        await message.answer(f"{data.get('ENG')}"+"\nShare your phone number for authentication.", reply_markup=contact_eng)

    except requests.exceptions.RequestException as e:
        result = f"Request failed: {e}"
        await message.answer(f"sizdagi xatolik{result}")




    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def uzb_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = message.contact.phone_number
        chat_id =  message.from_user.id
        params = {
            'type': 'phone',
            'chat_id': chat_id,
            'phone_number': phone_number,
            'language':lan
        }
        try:
            response = requests.get(api_url, params=params, headers=headers)
            if response.ok:
                if 'application/json' in response.headers.get('Content-Type', ''):
                    data = response.json()
                    p = data.get("RU")
                    result = response.text
                    await message.answer(f"{p}", reply_markup=user_eng)
                else:
                    result = f"Response is not in JSON format: {response.text}"
            else:
                result = f"Request failed with status code {response.status_code}: {response.reason}"
            # await message.answer(f"{data.get('UZ')}", reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            result = f"Request failed: {e}"
            await message.answer(f"{data.get('ENG')}")

    @dp.message_handler(text="Debt check ＄")
    async def tel1(message: types.Message):
        params = {
            "type": "contracts",
            "chat_id": message.from_user.id
        }
        response = requests.get(api_url, params=params, headers=headers)
        global ta
        ta = {}
        if response:
            data = response.json()
            if data is not None and 'contracts' in data and data['contracts']:
                buttons = []
                row = []
                for index, contract_info in enumerate(data['contracts'], start=1):
                    button_text = str(contract_info['contract'])
                    ta[str(contract_info['contract'])] = str(contract_info['contractID'])
                    button = KeyboardButton(text=button_text)
                    row.append(button)
                    if index % 2 == 0:
                        buttons.append([button])
                        row = []
                if row:
                    buttons.append(row)
                back_button = KeyboardButton(text="Back")
                buttons.append([back_button])
                reply_markup = ReplyKeyboardMarkup(keyboard=buttons)
                await message.answer("Choose which one of them", reply_markup=reply_markup)
                await Input.contracts.set()
            else:
                await message.answer("You haven't info yet", reply_markup=user_ru)
        else:
            await message.answer("Choose one of them: ", reply_markup=user_ru)

        @dp.message_handler(state=Input.contracts)
        async def tel2(message: types.Message, state: FSMContext):
            messa = message.text
            if messa != "Back":
                params = {
                    "type": "debt",
                    "chat_id": message.from_user.id
                }
                response = requests.get(api_url, params=params, headers=headers)
                if response:
                    data = response.json()
                    global summ, contract_id
                    contract = message.text
                    contract_id = ta[contract]
                    summ = data['allsumm']
                    val = data['currency']
                    for i in range(len(data['contracts'])):
                        if data['contracts'][i]['contract'] == contract:
                            contractsumm = data['contracts'][i]['contractsumm']
                            contractcurrency = data['contracts'][i]['contractcurrency']
                            contractekvivalent = data['contracts'][i]['contractekvivalent']
                    await message.answer(
                        f"Your total debt: {summ} {val},\n and this {contract}-contract information:\n{contractsumm} {contractcurrency}\n equivalence: {contractekvivalent}")
                    await state.finish()
                    await message.answer("Choose one of them: ", reply_markup=kop_eng)
            else:
                await message.answer('Back', reply_markup=user_eng)

                @dp.callback_query_handler(text='Yes')
                async def tel3(callback_query: types.CallbackQuery):
                    user_id = callback_query.from_user.id
                    date = str(datetime.datetime.today().date()) + "T00:00:00"
                    params = {
                        "type": "debt_check",
                        "chat_id": message.from_user.id,
                        "contract_id": contract_id,
                        "check": "true",
                        'summ': summ,
                        'date': date
                    }
                    response = requests.get(api_url, params=params, headers=headers)
                    if response:
                        data = response.json()
                        await bot.send_message(user_id, f"{data['succed_text']}", reply_markup = user_eng)

                @dp.callback_query_handler(text="No")
                async def tel4(callback_query: types.CallbackQuery):
                    user_id = callback_query.from_user.id
                    date = str(datetime.datetime.today().date()) + "T00:00:00"
                    params = {
                        "type": "debt_check",
                        "chat_id": message.from_user.id,
                        "contract_id": contract_id,
                        "check": "true",
                        'summ': summ,
                        'date': date
                    }
                    response = requests.get(api_url, params=params, headers=headers)
                    if response:
                        await bot.send_message(user_id, f"{data['succed_text']}", reply_markup = user_eng)

                @dp.callback_query_handler(text="Back")
                async def tel4(callback_query: types.CallbackQuery):
                    chat_id = callback_query.from_user.id
                    await bot.answer_callback_query(callback_query.id)
                    await bot.edit_message_reply_markup(chat_id=chat_id,
                                                        message_id=callback_query.message.message_id,
                                                        reply_markup=None)

    @dp.message_handler(text="Search by series")
    async def tel4(message: types.Message):
        await message.answer("Enter the serial number:")
        await Input.sery.set()

    @dp.message_handler(state=Input.sery)
    async def act(message: types.Message, state: FSMContext):
        global sery
        sery = message.text
        params = {
            "type": "search_by_series",
            "sery": sery,
            "chat_id": message.from_user.id
        }
        response = requests.get(api_url, params=params, headers=headers)
        if response:
            data = response.json()
            contragent = data['contragent']
            number = data['number']
            nomenclature = data['nomenclature']
            await message.answer(f"contragent: {contragent}\nNomer: {number}\nNomenclature: {nomenclature}")
            await state.finish()

    @dp.message_handler(text = 'Contact us 📞')
    async def admin(message: types.Message):
        await message.answer("Admin: @pm_hilol")

        @dp.message_handler(text='Acquiring an act 🧾') # qayta qayta bossa bo'lishi kk forga o'xshab
        async def start_handler(message: types.Message, state: FSMContext):
            params = {
                "type": "contracts",
                "chat_id": message.from_user.id
            }
            response = requests.get(api_url, params=params, headers=headers)
            global ta, calback
            ta =[]
            calback = []
            data = response.json()
            print("ctla", data['contracts'])
            buttons = []
            for contract_info in data['contracts']:
                button_text = str(contract_info['contract'])
                cal_back = str(contract_info['contractID'])
                ta.append(str(contract_info['contract']))
                calback.append(str(contract_info['contractID']))
                button = InlineKeyboardButton(text=button_text, callback_data=cal_back)
                buttons.append([button])
            hammasi = InlineKeyboardButton(text="All", callback_data="All")
            orqaga = InlineKeyboardButton(text="Back", callback_data="Back")
            buttons.append([hammasi])
            ta.append('All')
            calback.append('All')
            buttons.append([orqaga])
            ta.append('Back')
            calback.append('Back')

            reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
            await message.answer("Agreement", reply_markup=reply_markup)
            await state.set_state("waiting_for_contract")

        @dp.callback_query_handler(state = 'waiting_for_contract')
        async def act(callback_query: CallbackQuery, state: FSMContext):
            global msgcall
            msgcall = callback_query.data
            print(msgcall)
            if msgcall != "Back":
                await state.finish()
                await TimeInput.start_time.set()
                await callback_query.message.answer("Enter the start date (for example: YYYY-MM-DD): ")
            elif msgcall == "All":
                await state.finish()
                await TimeInput.start_time.set()
                await callback_query.message.answer("Enter the start date (for example: YYYY-MM-DD): ")
            else:
                await callback_query.message.edit_reply_markup(reply_markup=None)


        @dp.message_handler(state=TimeInput.start_time)
        async def start_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['start'] = message.text
                    global start_t
                    start_t = message.text
                    await TimeInput.next()
                    await message.answer("Enter the end date (for example: YYYY-MM-DD): ")
            else:
                await message.answer("Enter the date in the correct format (for example: Year-Month-Day): ")


        @dp.message_handler(state=TimeInput.end_time)
        async def end_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['finish'] = message.text
                    global start_t
                    start = start_t + 'T00:00:00'
                    finish = message.text + 'T00:00:00'
                    chat_id = message.from_user.id
                    if msgcall == 'Все':
                        if start_t < message.text:
                            params = {
                                "type": "reconciliation_act",
                                "chat_id": chat_id,
                                "start": start,
                                "finish": finish
                            }
                    if start_t < message.text:
                        params = {
                            "type": "reconciliation_act",
                                "chat_id": chat_id,
                                "start":start,
                                "finish":finish,
                                'contract_id':msgcall
                        }
                        response = requests.get(api_url, params=params, headers=headers)
                        try:
                            if response.ok:
                                content_type = response.headers.get('Content-Type', '')
                                if 'application/json' in content_type:
                                    data = response.json()
                                    if data.get('allsumm') is None:
                                        await message.answer("You don't have funds yet")
                                    else:
                                        await message.answer(f"{data['allsumm']}----{data['contracts']}")
                                    await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                                elif 'application/octet-stream' in content_type or 'application/vnd.ms-excel' in content_type:
                                    bio = io.BytesIO(response.content)
                                    bio.name = 'received_file.xlsx'
                                    await message.answer_document(document=bio)
                                else:
                                    result = f"Unknown Content-Type: {content_type}"
                                    await message.answer(f"Sizdagi xatolik {result}")
                            else:
                                result = f"Request failed with status code {response.status_code}: {response.reason}"
                                # print("error", result)
                                await message.answer(f"Sizdagi xatolik {result}")

                        except requests.exceptions.RequestException as e:
                            result = f"Request failed: {e}"
                            await message.answer(f"Sizdagi xatolik exepdan {result}")
                        await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                        await state.finish()
                    else:
                        await message.answer("The start date is greater than the end date!")
                        await TimeInput.start_time.set()
                        await message.answer("Enter the start date (for example: YYYY-MM-DD):")








if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)