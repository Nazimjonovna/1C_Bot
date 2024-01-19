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
# from dotenv import load_dotenv
# load_dotenv()
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Your API endpoint URL

api_url = 'http://localhost:8081/juramix'
login = 'Maxdecoruz'
password = '0ut0fb0unD'

# Token of tg_Bot
# API_TOKEN = '6619844226:AAFUabaziFZyL70r3dmcF1eHBU66dA1y4Fo'

API_TOKEN = '6293716593:AAEag5wzWypCJTJa1EzUoRsUO6MVx0ufMNA'

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
                    if p is not None:
                        result = response.text
                        await message.answer(f"{p}", reply_markup=user_uz)
                    else:
                        await message.answer(f"Uzr xurmatli mijoz siz haqingizda ma'lumot topilmadi.\nAdminlarimizga murojaat etishingizni so'rab qolamiz|@pm_hilol", reply_markup=start_t)
                else:
                    result = f"Response is not in JSON format: {response.text}"
            else:
                result = f"Request failed with status code {response.status_code}: {response.reason}"
            # await message.answer(f"{data.get('UZ')}", reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            result = f"Request failed: {e}"
            await message.answer(f"{data.get('UZ')}")

    @dp.message_handler(text="Qarzdorlikni tekshirish") # TODO this inlinekeyboard button
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
                    callback_text = str(contract_info['contractID'])
                    ta[str(contract_info['contract'])] = str(contract_info['contractID'])
                    button = InlineKeyboardButton(text=button_text, callback_data = callback_text)
                    row.append(button)
                    if index % 2 == 0:
                        buttons.append([button])
                        row = []
                if row:
                    buttons.append(row)
                back_button = InlineKeyboardButton(text="Orqaga", callback_data='Orqaga')
                buttons.append([back_button])
                reply_markup = InlineKeyboardMarkup(inline_keyboard = buttons)
                await message.answer("Choose which one of them", reply_markup=reply_markup)
                await Input.contracts.set()
            else:
                await message.answer("data yoq sizda", reply_markup=user_uz)
        else:
            await message.answer("Quyidagilardan tanlang: ", reply_markup=user_uz)

        @dp.callback_query_handler(state=Input.contracts)
        async def tel2(call: types.CallbackQuery, state: FSMContext):
            global messa
            messa = call.data
            k = next(key for key, value in ta.items() if value == messa)
            if messa != "Orqaga":
                params = {
                    "type": "debt",
                    "chat_id": message.from_user.id
                }
                response = requests.get(api_url, params=params, headers=headers)
                if response:
                    data = response.json()
                    global summ, contract_id
                    contract_id = k
                    summ = data['allsumm']
                    val = data['currency']
                    for i in range(len(data['contracts'])):
                        if data['contracts'][i]['contract'] == contract_id:
                            contractsumm = data['contracts'][i]['contractsumm']
                            contractcurrency = data['contracts'][i]['contractcurrency']
                            contractekvivalent = data['contracts'][i]['contractekvivalent']
                    if contractsumm is not None:
                        message_text = f"Sizning jammi qarzdorligingiz: {summ} {val},\n va ushbu {contract_id}-shartnomasi bo'yicha ma'lumotlar:\n{contractsumm} {contractcurrency}\n ekvvivaletligi: {contractekvivalent}"
                        await bot.send_message(chat_id=chat_id, text = message_text)
                        await state.finish()
                        await bot.send_message(message.chat.id, "Quyidagilardan tanlang: ", reply_markup=kop)
                    else:
                        await bot.send_message(chat_id=chat_id, text = message_text)
            else:
                await bot.send_message(message.chat.id, 'Orqaga', reply_markup=user_uz)

        @dp.callback_query_handler(text='Xa')
        async def tel3(callback_query: types.CallbackQuery):
            user_id = callback_query.from_user.id
            date = str(datetime.datetime.today().date()) + "T00:00:00"
            params = {
                "type": "debt_check",
                "chat_id": callback_query.from_user.id,
                "contract_id": messa,
                "check": "true",
                'summ': summ,
                'date': date
            }
            print(params)
            response = requests.get(api_url, params=params, headers=headers)
            if response.ok:
                print("kk", response.status_code)
                data = response.json()
                await bot.send_message(user_id, f"{data['succed_text']}")
                await bot.edit_message_reply_markup(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    reply_markup=None
                )
                await bot.send_message(user_id, "Quyidagilardan birini tanlang: ", reply_markup=user_uz)


        @dp.callback_query_handler(text="Yo'q")
        async def tel4(callback_query: types.CallbackQuery):
            user_id = callback_query.from_user.id
            date = str(datetime.datetime.today().date()) + "T00:00:00"
            params = {
                "type": "debt_check",
                "chat_id": message.from_user.id,
                "contract_id": messa,
                "check": "true",
                'summ': summ,
                'date': date
            }
            response = requests.get(api_url, params=params, headers=headers)
            if response:
                await bot.send_message(user_id, f"{data['succed_text']}")
                await bot.edit_message_reply_markup(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    reply_markup=None
                )
                await bot.send_message(user_id, "Quyidagilardan birini tanlang: ", reply_markup=user_uz)

        @dp.callback_query_handler(text="Orqaga")
        async def tel4(callback_query: types.CallbackQuery):
            chat_id = callback_query.from_user.id
            await bot.answer_callback_query(callback_query.id)
            await bot.edit_message_reply_markup(chat_id=chat_id,
                                                message_id=callback_query.message.message_id,
                                                reply_markup=None)

    # @dp.message_handler(text="Seriya bo'yicha izlash")
    # async def tel4(message: types.Message):
    #     await message.answer("Seriya raqamini kiriting:")
    #     await Input.sery.set()

    # @dp.message_handler(state=Input.sery)
    # async def act(message: types.Message, state: FSMContext):
    #     global sery
    #     sery = message.text
    #     params = {
    #         "type": "search_by_series",
    #         "sery": sery,
    #         "chat_id": message.from_user.id
    #     }
    #     response = requests.get(api_url, params=params, headers=headers)
    #     if response:
    #         data = response.json()
    #         print(data)
    #         if 'contragent' in data:
    #             contragent = data['contragent']
    #             number = data['number']
    #             nomenclature = data['nomenclature']
    #             await message.answer(f"Xaridor: {contragent}\nTelefon_nomeri: {number}\nTovar: {nomenclature}")
    #             await state.finish()
    #         else:
    #             await state.finish()
    #             await message.answer("Ushbu seriya raqam bo'yicha ma'lumot topilmadi", reply_markup=user_uz)

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
                    if p is not None:
                        await message.answer(f"{p}", reply_markup=user_ru)
                    else:
                        await message.answer(f"Извините, уважаемый клиент, никакой информации о Вас не найдено.\nПожалуйста, свяжитесь с нашими администраторами.|@pm_hilol", reply_markup=start_t)
                else:
                    result = f"Response is not in JSON format: {response.text}"
            else:
                result = f"Request failed with status code {response.status_code}: {response.reason}"
            # await message.answer(f"{data.get('UZ')}", reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            result = f"Request failed: {e}"
            await message.answer(f"{data.get('RU')}")


    @dp.message_handler(text="Проверка долга ＄") # TODO this inlinekeyboard button
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
                    callback_text = str(contract_info['contractID'])
                    ta[str(contract_info['contract'])] = str(contract_info['contractID'])
                    button = InlineKeyboardButton(text=button_text, callback_data = callback_text)
                    row.append(button)
                    if index % 2 == 0:
                        buttons.append([button])
                        row = []
                if row:
                    buttons.append(row)
                back_button = InlineKeyboardButton(text="Назад", callback_data='Назад')
                buttons.append([back_button])
                reply_markup = InlineKeyboardMarkup(inline_keyboard = buttons)
                await message.answer("Choose which one of them", reply_markup=reply_markup)
                await Input.contracts.set()
            else:
                await message.answer("data yoq sizda", reply_markup=user_ru)
        else:
            await message.answer("Выберите из следующих: ", reply_markup=user_ru)

        @dp.callback_query_handler(state=Input.contracts)
        async def tel2(call: types.CallbackQuery, state: FSMContext):
            messa = call.data
            k = next(key for key, value in ta.items() if value == messa)
            if messa != "Назад":
                params = {
                    "type": "debt",
                    "chat_id": message.from_user.id
                }
                response = requests.get(api_url, params=params, headers=headers)
                if response:
                    data = response.json()
                    global summ, contract_id
                    contract_id = k
                    summ = data['allsumm']
                    val = data['currency']
                    for i in range(len(data['contracts'])):
                        if data['contracts'][i]['contract'] == contract_id:
                            contractsumm = data['contracts'][i]['contractsumm']
                            contractcurrency = data['contracts'][i]['contractcurrency']
                            contractekvivalent = data['contracts'][i]['contractekvivalent']
                    if contractsumm is not None:
                        message_text = f"Ваш общий долг: {summ} {val},\n и это {contract_id}-информация о контракте:\n{contractsumm} {contractcurrency}\n эквивалентность: {contractekvivalent}"
                        await bot.send_message(chat_id=chat_id, text = message_text)
                        await state.finish()
                        await bot.send_message(message.chat.id, "Выберите из следующих:  ", reply_markup=kop_ru)
                    else:
                        await bot.send_message(chat_id=chat_id, text = message_text)
            else:
                await bot.send_message(message.chat.id, 'Orqaga', reply_markup=user_ru)

        @dp.callback_query_handler(text='Да')
        async def tel3(callback_query: types.CallbackQuery):
            user_id = callback_query.from_user.id
            date = str(datetime.datetime.today().date()) + "T00:00:00"
            params = {
                "type": "debt_check",
                "chat_id": callback_query.from_user.id,
                "contract_id": messa,
                "check": "true",
                'summ': summ,
                'date': date
            }
            print(params)
            response = requests.get(api_url, params=params, headers=headers)
            if response.ok:
                print("kk", response.status_code)
                data = response.json()
                await bot.send_message(user_id, f"{data['succed_text']}")
                await bot.edit_message_reply_markup(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    reply_markup=None
                )
                await bot.send_message(user_id, "Выберите из следующих:  ", reply_markup=user_ru)
            else:
                await bot.send_message(user_id, "ehhh")


        @dp.callback_query_handler(text="Нет")
        async def tel4(callback_query: types.CallbackQuery):
            user_id = callback_query.from_user.id
            date = str(datetime.datetime.today().date()) + "T00:00:00"
            params = {
                "type": "debt_check",
                "chat_id": message.from_user.id,
                "contract_id": messa,
                "check": "true",
                'summ': summ,
                'date': date
            }
            response = requests.get(api_url, params=params, headers=headers)
            if response:
                await bot.send_message(user_id, f"{data['succed_text']}")
                await bot.edit_message_reply_markup(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    reply_markup=None
                )
                await bot.send_message(user_id, "Выберите из следующих:  ", reply_markup=user_ru)

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
            if 'contragent' in data:
                contragent = data['contragent']
                number = data['number']
                nomenclature = data['nomenclature']
                await message.answer(f"Покупатель: {contragent}\nHомер телефона: {number}\nTовар: {nomenclature}")
                await state.finish()
            else:
                await state.finish()
                await message.answer("Для этого серийного номера информация не найдена", reply_markup=user_uz)

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
                    if p is not None:
                        await message.answer(f"{p}", reply_markup=user_eng)
                    else:
                        await message.answer(f"Sorry, dear client, no information about you was found.\nPlease contact our administrators.|@pm_hilol", reply_markup=start_t)
                else:
                    result = f"Response is not in JSON format: {response.text}"
            else:
                result = f"Request failed with status code {response.status_code}: {response.reason}"
            # await message.answer(f"{data.get('UZ')}", reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            result = f"Request failed: {e}"
            await message.answer(f"{data.get('ENG')}")

    @dp.message_handler(text="Debt check ＄") # TODO this inlinekeyboard button
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
                    callback_text = str(contract_info['contractID'])
                    ta[str(contract_info['contract'])] = str(contract_info['contractID'])
                    button = InlineKeyboardButton(text=button_text, callback_data = callback_text)
                    row.append(button)
                    if index % 2 == 0:
                        buttons.append([button])
                        row = []
                if row:
                    buttons.append(row)
                back_button = InlineKeyboardButton(text="Back", callback_data='Back')
                buttons.append([back_button])
                reply_markup = InlineKeyboardMarkup(inline_keyboard = buttons)
                await message.answer("Choose which one of them", reply_markup=reply_markup)
                await Input.contracts.set()
            else:
                await message.answer("data yoq sizda", reply_markup=user_eng)
        else:
            await message.answer("Choose one of them: ", reply_markup=user_eng)

        @dp.callback_query_handler(state=Input.contracts)
        async def tel2(call: types.CallbackQuery, state: FSMContext):
            messa = call.data
            k = next(key for key, value in ta.items() if value == messa)
            if messa != "Back":
                params = {
                    "type": "debt",
                    "chat_id": message.from_user.id
                }
                response = requests.get(api_url, params=params, headers=headers)
                if response:
                    data = response.json()
                    global summ, contract_id
                    contract_id = k
                    summ = data['allsumm']
                    val = data['currency']
                    for i in range(len(data['contracts'])):
                        if data['contracts'][i]['contract'] == contract_id:
                            contractsumm = data['contracts'][i]['contractsumm']
                            contractcurrency = data['contracts'][i]['contractcurrency']
                            contractekvivalent = data['contracts'][i]['contractekvivalent']
                    if contractsumm is not None:
                        message_text = f"Your totel debt: {summ} {val},\n and this {contract_id}-information of contracts:\n{contractsumm} {contractcurrency}\n ekvivalents: {contractekvivalent}"
                        await bot.send_message(chat_id=chat_id, text = message_text)
                        await state.finish()
                        await bot.send_message(message.chat.id, "Choose one of this:  ", reply_markup=kop_eng)
                    else:
                        await bot.send_message(chat_id=chat_id, text = message_text)
            else:
                await bot.send_message(message.chat.id, 'Back', reply_markup=user_eng)

        @dp.callback_query_handler(text='Yes')
        async def tel3(callback_query: types.CallbackQuery):
            user_id = callback_query.from_user.id
            date = str(datetime.datetime.today().date()) + "T00:00:00"
            params = {
                "type": "debt_check",
                "chat_id": callback_query.from_user.id,
                "contract_id": messa,
                "check": "true",
                'summ': summ,
                'date': date
            }
            print(params)
            response = requests.get(api_url, params=params, headers=headers)
            if response.ok:
                print("kk", response.status_code)
                data = response.json()
                await bot.send_message(user_id, f"{data['succed_text']}")
                await bot.edit_message_reply_markup(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    reply_markup=None
                )
                await bot.send_message(user_id, "Choose one of this:  ", reply_markup=user_ru)
            else:
                await bot.send_message(user_id, "ehhh")


        @dp.callback_query_handler(text="No")
        async def tel4(callback_query: types.CallbackQuery):
            user_id = callback_query.from_user.id
            date = str(datetime.datetime.today().date()) + "T00:00:00"
            params = {
                "type": "debt_check",
                "chat_id": message.from_user.id,
                "contract_id": messa,
                "check": "true",
                'summ': summ,
                'date': date
            }
            response = requests.get(api_url, params=params, headers=headers)
            if response:
                await bot.send_message(user_id, f"{data['succed_text']}")
                await bot.edit_message_reply_markup(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    reply_markup=None
                )
                await bot.send_message(user_id, "Choose one of this:  ", reply_markup=user_ru)

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
            if 'contragent' in data:
                contragent = data['contragent']
                number = data['number']
                nomenclature = data['nomenclature']
                await message.answer(f"contragent: {contragent}\nNomer: {number}\nNomenclature: {nomenclature}")
                await state.finish()
            else:
                await state.finish()
                await message.answer("No information found for this serial number", reply_markup=user_uz)

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