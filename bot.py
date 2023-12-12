import logging
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
API_TOKEN ='Shakhlo)))'

headers = {
            'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
            'User-Agent': 'PostmanRuntime/7.35.0',
            'Accept': '*/*',
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


@dp.message_handler(text = "Uzb")
async def uzb(message: types.Message):
    await message.answer("Assalomu alaykum, OOO APPLOAD CRM botiga xush kelibsiz!\nIdentifikatsiyadan o’tish uchun telefon raqamingizni ulashing.", reply_markup=contact_uz)



    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def uzb_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = message.contact.phone_number
        chat_id =  message.from_user.id
        print(chat_id)
        params = {
            'type': 'phone',
            'chat_id': chat_id,
            'phone_number': phone_number
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
            await message.answer(f"{data.get('UZ')}", reply_markup=user_uz)

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
                for contract_info in data['contracts']:
                    button_text = str(contract_info['contract'])
                    ta[str(contract_info['contract'])] = str(contract_info['contractID'])
                    button = KeyboardButton(text=button_text)
                    buttons.append([button])
                reply_markup = ReplyKeyboardMarkup(keyboard=buttons)
                await message.answer("Choose which one of them", reply_markup=reply_markup)
                await Input.contracts.set()
            else:
                await message.answer("data yoq sizda", reply_markup=menu)
        else:
            await message.answer("Quyidagilardan tanlang: ", reply_markup=menu)

        @dp.message_handler(state=Input.contracts)
        async def tel2(message: types.Message, state: FSMContext):
            params = {
                "type": "debt",
                "chat_id": message.from_user.id
            }
            response = requests.get(api_url, params=params, headers=headers)
            print(response.json())
            if response:
                data = response.json()
                global summ, contract_id
                contract = message.text
                print(contract)
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
async def ru(message: types.Message):
    await message.answer("Здравствуйте, добро пожаловать в бот ООО «Апплоад CRM»!\nПоделитесь своим номером телефона для аутентификации.", reply_markup=contact_ru)

    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def ru_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = message.contact.phone_number
        chat_id = message.from_user.id
        params = {
            'type': 'phone',
            'chat_id': 901569590,
            'phone_number': '+998933411945'
        }
        headers = {
            'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
            'User-Agent': 'PostmanRuntime/7.35.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        try:
            response = requests.get(api_url, params=params, headers=headers)
            if response.ok:
                if 'application/json' in response.headers.get('Content-Type', ''):
                    data = response.json()
                    print(data)
                    result = response.text
                else:
                    result = f"Response is not in JSON format: {response.text}"
            else:
                result = f"Request failed with status code {response.status_code}: {response.reason}"
            await message.answer(f"{data.get('RU')}", reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            result = f"Request failed: {e}"
            await message.answer(f"{data.get('RU')}")



        @dp.message_handler(text='Проверка долга ＄')
        async def ru_baz(message: types.Message):
            chat_id =message.from_user.id
            params = {
                'type': 'contracts',
                'chat_id': 901569590
            }
            headers = {
                'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                'User-Agent': 'PostmanRuntime/7.35.0',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            try:
                response = requests.get(api_url, params=params, headers=headers)
                if response.ok:
                    if 'application/json' in response.headers.get('Content-Type', ''):
                        data = response.json()
                        con = {}
                        for i in data.get('contracts'):
                            for k, v in i.items():
                                con[k] = v
                                await message.answer(f"{k}---{v}".format())
                        result = response.text
                    else:
                        result = f"Response is not in JSON format: {response.text}"
                        await message.answer(f"ошибка {result}")
                else:
                    result = f"Request failed with status code {response.status_code}: {response.reason}"
                    await message.answer(f"ошибка {result}")

            except requests.exceptions.RequestException as e:
                result = f"Request failed: {e}"
                await message.answer(f"ошибка {result}")
            await message.answer(f"Выберите один из следующих разделов:", reply_markup=c_button_ru)

            @dp.message_handler(text = 'AllSumm')
            async def all(message: types.Message):
                chat_id = message.from_user.id
                params = {
                    'type': 'debt',
                    'chat_id': 901569590
                }
                headers = {
                    'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                    'User-Agent': 'PostmanRuntime/7.35.0',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                try:
                    response = requests.get(api_url, params=params, headers=headers)
                    if response.ok:
                        if 'application/json' in response.headers.get('Content-Type', ''):
                            data = response.json()
                            print("Mana", data)
                            for key, value in data.items():
                                if data['allsumm'] == None:
                                    await message.answer("У вас еще нет средств")
                                else:
                                    await message.answer(f"{data['allsumm']}----{data['contracts']}")
                            result = response.text
                        else:
                            result = f"Response is not in JSON format: {response.text}"
                            await message.answer(f"Oшибка--{result}")
                    else:
                        result = f"Request failed with status code {response.status_code}: {response.reason}"
                        await message.answer(f"Oшибка--{result}")

                except requests.exceptions.RequestException as e:
                    result = f"Request failed: {e}"
                    await message.answer(f"Oшибка--{result}")

            @dp.message_handler(text = 'Вернуться в главное меню 🔙')
            async def back(message: types.Message):
                await message.answer(text = "Orqaga",reply_markup=user_ru)

        @dp.message_handler(text='Связаться с нами 📞')
        async def admin(message: types.Message):
            await message.answer("Admin: @pm_hilol")

        @dp.message_handler(text='Приобретение акта 🧾')
        async def start_handler(message: types.Message, state: FSMContext):
            params = {
                "type": "contracts",
                "chat_id": 901569590
            }
            headers = {
                'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                'User-Agent': 'PostmanRuntime/7.35.0',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            response = requests.get(api_url, params=params, headers=headers)
            global ta
            ta = []
            data = response.json()
            buttons = []
            # global contract_info
            for contract_info in data['contracts']:
                button_text = str(contract_info['contract'])
                ta.append(str(contract_info['contract']))
                button = KeyboardButton(text=button_text)
                buttons.append([button])
            buttons.append(['все'])
            buttons.append(['создавать новое'])

            reply_markup = ReplyKeyboardMarkup(keyboard=buttons)
            await message.answer("в соответствии с которым", reply_markup=reply_markup)
            await state.set_state("waiting_for_contract")

        @dp.message_handler(state="waiting_for_contract")
        async def act(message: types.Message, state: FSMContext):
            selected_contract = message.text
            print("msg", selected_contract)
            print(ta)
            if selected_contract in ta or selected_contract == 'все':
                params = {
                    "type": "reconciliation_act",
                    "chat_id": 901569590
                }
                headers = {
                    'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                    'User-Agent': 'PostmanRuntime/7.35.0',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                response = requests.get(api_url, params=params, headers=headers)
                try:
                    if response.ok:
                        content_type = response.headers.get('Content-Type', '')
                        if 'application/json' in content_type:
                            data = response.json()
                            if data.get('allsumm') is None:
                                await message.answer("У вас еще нет средств ")
                            else:
                                await message.answer(f"{data['allsumm']}----{data['contracts']}")
                        elif 'application/octet-stream' in content_type or 'application/vnd.ms-excel' in content_type:
                            bio = io.BytesIO(response.content)
                            bio.name = 'received_file.xlsx'
                            await message.answer_document(document=bio)
                        else:
                            result = f"Unknown Content-Type: {content_type}"
                            print('error0', result)
                            await message.answer(f"ошибка---{result}")
                    else:
                        result = f"Request failed with status code {response.status_code}: {response.reason}"
                        # print("error", result)
                        await message.answer(f"ошибка---{result}")

                except requests.exceptions.RequestException as e:
                    result = f"Request failed: {e}"
                    await message.answer(f"ошибка---{result}")
            else:
                await TimeInput.start_time.set()
                await message.answer("Введите дату начала:")

        @dp.message_handler(state=TimeInput.start_time)
        async def start_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['start'] = message.text
                    global start_t
                    start_t = message.text
                    await TimeInput.next()
                    await message.answer("Введите дату окончания:")
            else:
                await message.answer("Введите дату в неправильном формате (чч:мм):")

        @dp.message_handler(state=TimeInput.end_time)
        async def end_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['finish'] = message.text
                    global start_t
                    print(type(message.text))
                    start = start_t + 'T00:00:00'
                    finish = message.text + 'T00:00:00'
                    print(finish)
                    chat_id = message.from_user.id
                    params = {
                        "type": "reconciliation_act",
                        "chat_id": 901569590,
                        "start": start,
                        "finish": finish
                    }
                    headers = {
                        'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                        'User-Agent': 'PostmanRuntime/7.35.0',
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive'
                    }
                    response = requests.get(api_url, params=params, headers=headers)
                    try:
                        if response.ok:
                            content_type = response.headers.get('Content-Type', '')
                            if 'application/json' in content_type:
                                data = response.json()
                                if data.get('allsumm') is None:
                                    await message.answer("У вас еще нет средств ")
                                else:
                                    await message.answer(f"{data['allsumm']}----{data['contracts']}")
                                await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                            elif 'application/octet-stream' in content_type or 'application/vnd.ms-excel' in content_type:
                                bio = io.BytesIO(response.content)
                                bio.name = 'received_file.xlsx'
                                await message.answer_document(document=bio)
                            else:
                                result = f"Unknown Content-Type: {content_type}"
                                print('error0', result)
                                await message.answer(f"ошибка---{result}")
                        else:
                            result = f"Request failed with status code {response.status_code}: {response.reason}"
                            await message.answer(f"ошибка---{result}")

                    except requests.exceptions.RequestException as e:
                        result = f"Request failed: {e}"
                        await message.answer(f"ошибка---{result}")
                    await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                    await state.finish()





























@dp.message_handler(text = "🇬🇧")
async def eng(message: types.Message):
    await message.answer("Hello, welcome to OOO APPLOAD CRM bot!\nShare your phone number for authentication.", reply_markup=contact_eng)
    #bazani tekshir
    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def eng_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = message.contact.phone_number
        chat_id = message.from_user.id
        params = {
            'type': 'phone',
            'chat_id': 901569590,
            'phone_number': '+998933411945'
        }
        headers = {
            'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
            'User-Agent': 'PostmanRuntime/7.35.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
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
            await message.answer(f"{data.get('ENG')}", reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            result = f"Request failed: {e}"

            await message.answer(f"{data.get('ENG')}")



        @dp.message_handler(text='Debt check ＄')
        async def ru_baz(message: types.Message):
            chat_id = message.from_user.id
            params = {
                'type': 'contracts',
                'chat_id': 901569590
            }
            headers = {
                'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                'User-Agent': 'PostmanRuntime/7.35.0',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            try:
                response = requests.get(api_url, params=params, headers=headers)
                if response.ok:
                    if 'application/json' in response.headers.get('Content-Type', ''):
                        data = response.json()
                        for key, value in data.items():
                            if data['allsumm'] == None:
                                await message.answer("Sizda hozircha mablag' yo ")
                            else:
                                await message.answer(f"{data['allsumm']}----{data['contracts']}")
                        # con = {}
                        # for i in data.get('contracts'):
                        #     for k, v in i.items():
                        #         con[k] = v
                        #         await message.answer(f"{k}---{v}".format())
                        result = response.text
                    else:
                        result = f"Response is not in JSON format: {response.text}"
                        await message.answer(f"Your error is {result}")
                else:
                    result = f"Request failed with status code {response.status_code}: {response.reason}"
                    await message.answer(f"Your error is {result}")

            except requests.exceptions.RequestException as e:
                result = f"Request failed: {e}"
                await message.answer(f"Your error is {result}")
            await message.answer(f"Choose one of the following sections:", reply_markup=c_button_eng)

            @dp.message_handler(text = 'AllSumm')
            async def all(message: types.Message):
                chat_id = message.from_user.id
                params = {
                    'type': 'debt',
                    'chat_id': 901569590
                }
                headers = {
                    'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                    'User-Agent': 'PostmanRuntime/7.35.0',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                try:
                    response = requests.get(api_url, params=params, headers=headers)
                    if response.ok:
                        if 'application/json' in response.headers.get('Content-Type', ''):
                            data = response.json()
                            print("Mana", data)
                            for key, value in data.items():
                                if data['allsumm'] == None:
                                    await message.answer("You have not debt yet")
                                else:
                                    await message.answer(f"{data['allsumm']}----{data['contracts']}")
                            result = response.text
                        else:
                            result = f"Response is not in JSON format: {response.text}"
                            await message.answer(f"Error--{result}")
                    else:
                        result = f"Request failed with status code {response.status_code}: {response.reason}"
                        await message.answer(f"Error--{result}")

                except requests.exceptions.RequestException as e:
                    result = f"Request failed: {e}"
                    await message.answer(f"Error--{result}")

            @dp.message_handler(text = 'Return to main menu 🔙')
            async def back(message: types.Message):
                await message.answer(text = "Orqaga",reply_markup=user_eng)


        @dp.message_handler(text = 'Biz bilan bog’lanish 📞')
        async def admin(message: types.Message):
            await message.answer("Admin: @pm_hilol")

        @dp.message_handler(text='Akt sverka olish 🧾')
        async def start_handler(message: types.Message, state: FSMContext):
            await TimeInput.start_time.set()
            await message.answer("Boshlang'ich sanani kiriting: ")


        @dp.message_handler(state=TimeInput.start_time)
        async def start_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['start'] = message.text
                    global start_t
                    start_t = message.text
                    await TimeInput.next()
                    await message.answer("Tugash sanani kiriting: ")
            else:
                await message.answer("Noto'g'ri formatda sanani kiriting (hh:mm): ")


        @dp.message_handler(state=TimeInput.end_time)
        async def end_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['finish'] = message.text
                    global start_t
                    print(type(message.text))
                    start = start_t + 'T00:00:00'
                    finish = message.text + 'T00:00:00'
                    print(finish)
                    chat_id = message.from_user.id
                    params = {
                    "type": "reconciliation_act",
                        "chat_id": 901569590,
                        "start":start,
                        "finish":finish
                }
                headers = {
                    'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                    'User-Agent': 'PostmanRuntime/7.35.0',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                response = requests.get(api_url, params=params, headers=headers)
                print(response.content)
                print(params)
                try:
                    if response.ok:
                        content_type = response.headers.get('Content-Type', '')
                        if 'application/json' in content_type:
                            data = response.json()
                            # Process JSON data here
                            if data.get('allsumm') is None:
                                await message.answer("Sizda hozircha mablag' yo ")
                            else:
                                await message.answer(f"{data['allsumm']}----{data['contracts']}")
                            await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                        elif 'application/octet-stream' in content_type or 'application/vnd.ms-excel' in content_type:
                            # If the response is a file or binary data (including Excel files)
                            bio = io.BytesIO(response.content)
                            bio.name = 'received_file.xlsx'  # You can specify the file name based on your needs
                            await message.answer_document(document=bio)
                        else:
                            result = f"Unknown Content-Type: {content_type}"
                            print('error0', result)
                            await message.answer(f"Sizdagi xatolik {result}")
                    else:
                        result = f"Request failed with status code {response.status_code}: {response.reason}"
                        print("error", result)
                        await message.answer(f"Sizdagi xatolik {result}")

                except requests.exceptions.RequestException as e:
                    result = f"Request failed: {e}"
                    await message.answer(f"Sizdagi xatolik exepdan {result}")
                await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                await state.finish()
                    
            else:
                await message.answer("Noto'g'ri formatda sanani kiriting (hh:mm): ")






















@dp.message_handler(text = "🇷🇺")
async def ru(message: types.Message):
    await message.answer("Здравствуйте, добро пожаловать в бот ООО «Апплоад CRM»!\nПоделитесь своим номером телефона для аутентификации.", reply_markup=contact_ru)

    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def ru_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = message.contact.phone_number
        chat_id = message.from_user.id
        params = {
            'type': 'phone',
            'chat_id': 901569590,
            'phone_number': '+998933411945'
        }
        headers = {
            'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
            'User-Agent': 'PostmanRuntime/7.35.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
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
            await message.answer(f"{data.get('RU')}", reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            result = f"Request failed: {e}"

            await message.answer(f"{data.get('RU')}")



        @dp.message_handler(text='Проверка долга ＄')
        async def ru_baz(message: types.Message):
            chat_id =message.from_user.id
            params = {
                'type': 'contracts',
                'chat_id': 901569590
            }
            headers = {
                'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                'User-Agent': 'PostmanRuntime/7.35.0',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            try:
                response = requests.get(api_url, params=params, headers=headers)
                if response.ok:
                    if 'application/json' in response.headers.get('Content-Type', ''):
                        data = response.json()
                        con = {}
                        for i in data.get('contracts'):
                            for k, v in i.items():
                                con[k] = v
                                await message.answer(f"{k}---{v}".format())
                        result = response.text
                    else:
                        result = f"Response is not in JSON format: {response.text}"
                        await message.answer(f"Это твоя ошибка {result}")
                else:
                    result = f"Request failed with status code {response.status_code}: {response.reason}"
                    await message.answer(f"Это твоя ошибка {result}")

            except requests.exceptions.RequestException as e:
                result = f"Request failed: {e}"
                await message.answer(f"Sizdagi xatolik {result}")
            await message.answer(f"Выберите один из следующих разделов:", reply_markup=c_button_ru)

            @dp.message_handler(text = 'AllSumm')
            async def all(message: types.Message):
                chat_id = message.from_user.id
                params = {
                    'type': 'debt',
                    'chat_id': 901569590
                }
                headers = {
                    'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                    'User-Agent': 'PostmanRuntime/7.35.0',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                try:
                    response = requests.get(api_url, params=params, headers=headers)
                    if response.ok:
                        if 'application/json' in response.headers.get('Content-Type', ''):
                            data = response.json()
                            print("Mana", data)
                            for key, value in data.items():
                                if data['allsumm'] == None:
                                    await message.answer("У вас еще нет средств")
                                else:
                                    await message.answer(f"{data['allsumm']}----{data['contracts']}")
                            result = response.text
                        else:
                            result = f"Response is not in JSON format: {response.text}"
                            await message.answer(f"Oшибка--{result}")
                    else:
                        result = f"Request failed with status code {response.status_code}: {response.reason}"
                        await message.answer(f"Oшибка--{result}")

                except requests.exceptions.RequestException as e:
                    result = f"Request failed: {e}"
                    await message.answer(f"Oшибка--{result}")

            @dp.message_handler(text = 'Вернуться в главное меню 🔙')
            async def back(message: types.Message):
                await message.answer(text = "Orqaga",reply_markup=user_ru)

        @dp.message_handler(text='Связаться с нами 📞')
        async def admin(message: types.Message):
            await message.answer("Admin: @pm_hilol")

        @dp.message_handler(text='Приобретение акта 🧾')
        async def start_handler(message: types.Message, state: FSMContext):
            await TimeInput.start_time.set()
            await message.answer("Введите дату начала: ")


        @dp.message_handler(state=TimeInput.start_time)
        async def start_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['start'] = message.text
                    global start_t
                    start_t = message.text
                    await TimeInput.next()
                    await message.answer("Введите дату окончания: ")
            else:
                await message.answer("Введите дату в неправильном формате (чч:мм): ")


        @dp.message_handler(state=TimeInput.end_time)
        async def end_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['finish'] = message.text
                    global start_t
                    print(type(message.text))
                    a = start_t + 'T00:00:00'
                    f = message.text + 'T00:00:00'
                    start = datetime.strptime(a, "%Y-%m-%dT%H:%M:%S")
                    finish = datetime.strptime(f, "%Y-%m-%dT%H:%M:%S")
                    start_formatted = start.strftime("%Y-%m-%d %H:%M:%S")
                    finish_formatted = finish.strftime("%Y-%m-%d %H:%M:%S")
                    chat_id = message.from_user.id
                    params = {
                    "type": "reconciliation_act",
                        "chat_id": chat_id,
                        "start":start_formatted,
                        "finish":finish_formatted
                }
                headers = {
                    'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                    'User-Agent': 'PostmanRuntime/7.35.0',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                try:
                    response = requests.get(api_url, params=params, headers=headers)
                    if response.ok:
                        if 'application/json' in response.headers.get('Content-Type', ''):
                            data = response.json()
                            print("Mana", data)
                            for key, value in data.items():
                                if data['allsumm'] == None:
                                    await message.answer("У вас еще нет средств ")
                                else:
                                    await message.answer(f"{data['allsumm']}----{data['contracts']}")
                            result = response.text
                        else:
                            result = f"Response is not in JSON format: {response.text}"
                            await message.answer(f"Это твоя ошибка {result}")
                    else:
                        result = f"Request failed with status code {response.status_code}: {response.reason}"
                        await message.answer(f"Это твоя ошибка {result}")

                except requests.exceptions.RequestException as e:
                    result = f"Request failed: {e}"
                    await message.answer(f"Это твоя ошибка {result}")
                await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                await state.finish()
                    
            else:
                await message.answer("Введите дату в неправильном формате (чч:мм): ")
    
























@dp.message_handler(text = "🇬🇧")
async def eng(message: types.Message):
    await message.answer("Hello, welcome to OOO APPLOAD CRM bot!\nShare your phone number for authentication.", reply_markup=contact_eng)
    #bazani tekshir
    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def eng_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = message.contact.phone_number
        chat_id = message.from_user.id
        params = {
            'type': 'phone',
            'chat_id': 901569590,
            'phone_number': '+998933411945'
        }
        headers = {
            'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
            'User-Agent': 'PostmanRuntime/7.35.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
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
            await message.answer(f"{data.get('ENG')}", reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            result = f"Request failed: {e}"

            await message.answer(f"{data.get('ENG')}")



        @dp.message_handler(text='Debt check ＄')
        async def ru_baz(message: types.Message):
            chat_id = message.from_user.id
            params = {
                'type': 'contracts',
                'chat_id': 901569590
            }
            headers = {
                'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                'User-Agent': 'PostmanRuntime/7.35.0',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            try:
                response = requests.get(api_url, params=params, headers=headers)
                if response.ok:
                    if 'application/json' in response.headers.get('Content-Type', ''):
                        data = response.json()
                        con = {}
                        for i in data.get('contracts'):
                            for k, v in i.items():
                                con[k] = v
                                await message.answer(f"{k}---{v}".format())
                        result = response.text
                    else:
                        result = f"Response is not in JSON format: {response.text}"
                        await message.answer(f"Your error is {result}")
                else:
                    result = f"Request failed with status code {response.status_code}: {response.reason}"
                    await message.answer(f"Your error is {result}")

            except requests.exceptions.RequestException as e:
                result = f"Request failed: {e}"
                await message.answer(f"Your error is {result}")
            await message.answer(f"Choose one of the following sections:", reply_markup=c_button_eng)

            @dp.message_handler(text = 'AllSumm')
            async def all(message: types.Message):
                chat_id = message.from_user.id
                params = {
                    'type': 'debt',
                    'chat_id': 901569590
                }
                headers = {
                    'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                    'User-Agent': 'PostmanRuntime/7.35.0',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                try:
                    response = requests.get(api_url, params=params, headers=headers)
                    if response.ok:
                        if 'application/json' in response.headers.get('Content-Type', ''):
                            data = response.json()
                            print("Mana", data)
                            for key, value in data.items():
                                if data['allsumm'] == None:
                                    await message.answer("You have not debt yet")
                                else:
                                    await message.answer(f"{data['allsumm']}----{data['contracts']}")
                            result = response.text
                        else:
                            result = f"Response is not in JSON format: {response.text}"
                            await message.answer(f"Error--{result}")
                    else:
                        result = f"Request failed with status code {response.status_code}: {response.reason}"
                        await message.answer(f"Error--{result}")

                except requests.exceptions.RequestException as e:
                    result = f"Request failed: {e}"
                    await message.answer(f"Error--{result}")

            @dp.message_handler(text = 'Return to main menu 🔙')
            async def back(message: types.Message):
                await message.answer(text = "Orqaga",reply_markup=user_eng)


        @dp.message_handler(text='Contact us 📞')
        async def admin(message: types.Message):
            await message.answer("Admin: @pm_hilol")

        
        @dp.message_handler(text='Acquiring an act 🧾')
        async def start_handler(message: types.Message, state: FSMContext):

            params = {
                "type": "contracts",
                "chat_id": 901569590
            }
            headers = {
                'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                'User-Agent': 'PostmanRuntime/7.35.0',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            response = requests.get(api_url, params=params, headers=headers)
            global ta
            ta = []
            data = response.json()
            buttons = []
            for contract_info in data['contracts']:
                button_text = str(contract_info['contract'])
                ta.append(str(contract_info['contract']))
                button = KeyboardButton(text=button_text)
                buttons.append([button])
            buttons.append(['All'])
            buttons.append(['New'])

            reply_markup = ReplyKeyboardMarkup(keyboard=buttons)
            await message.answer("Choose which one of them", reply_markup=reply_markup)
            await state.set_state("waiting_for_contract")

        @dp.message_handler(state="waiting_for_contract")
        async def act(message: types.Message, state: FSMContext):
            selected_contract = message.text
            print("msg", selected_contract)
            print(ta)
            if selected_contract in ta or selected_contract == 'All':
                params = {
                    "type": "reconciliation_act",
                    "chat_id": 901569590
                }
                headers = {
                    'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                    'User-Agent': 'PostmanRuntime/7.35.0',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                response = requests.get(api_url, params=params, headers=headers)
                try:
                    if response.ok:
                        content_type = response.headers.get('Content-Type', '')
                        if 'application/json' in content_type:
                            data = response.json()
                            if data.get('allsumm') is None:
                                await message.answer("You have not debt yet")
                            else:
                                await message.answer(f"{data['allsumm']}----{data['contracts']}")
                        elif 'application/octet-stream' in content_type or 'application/vnd.ms-excel' in content_type:
                            bio = io.BytesIO(response.content)
                            bio.name = 'received_file.xlsx'
                            await message.answer_document(document=bio)
                        else:
                            result = f"Unknown Content-Type: {content_type}"
                            print('error0', result)
                            await message.answer(f"Error---{result}")
                    else:
                        result = f"Request failed with status code {response.status_code}: {response.reason}"
                        # print("error", result)
                        await message.answer(f"Error---{result}")

                except requests.exceptions.RequestException as e:
                    result = f"Request failed: {e}"
                    await message.answer(f"Error---{result}")
            else:
                await TimeInput.start_time.set()
                await message.answer("Enter beginning period: ")

            await TimeInput.start_time.set()
            await message.answer("Enter beginning period: ")



        @dp.message_handler(state=TimeInput.start_time)
        async def start_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['start'] = message.text
                    global start_t
                    start_t = message.text
                    await TimeInput.next()
                    await message.answer("Enter finishing time: ")
            else:
                await message.answer("Enter data in irregular format (chch:mm): ")

        @dp.message_handler(state=TimeInput.end_time)
        async def end_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
                async with state.proxy() as data:
                    data['finish'] = message.text
                    global start_t
                    print(type(message.text))

                    start = start_t + 'T00:00:00'
                    finish = message.text + 'T00:00:00'
                    print(finish)
                    chat_id = message.from_user.id
                    params = {
                        "type": "reconciliation_act",
                        "chat_id": 901569590,
                        "start": start,
                        "finish": finish
                    }
                    headers = {
                        'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                        'User-Agent': 'PostmanRuntime/7.35.0',
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive'
                    }
                    response = requests.get(api_url, params=params, headers=headers)
                    try:
                        if response.ok:
                            content_type = response.headers.get('Content-Type', '')
                            if 'application/json' in content_type:
                                data = response.json()
                                if data.get('allsumm') is None:
                                    await message.answer("You haven't debt yet")
                                else:
                                    await message.answer(f"{data['allsumm']}----{data['contracts']}")
                                await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                            elif 'application/octet-stream' in content_type or 'application/vnd.ms-excel' in content_type:
                                bio = io.BytesIO(response.content)
                                bio.name = 'received_file.xlsx'
                                await message.answer_document(document=bio)
                            else:
                                result = f"Unknown Content-Type: {content_type}"
                                print('error0', result)
                                await message.answer(f"Error---{result}")
                        else:
                            result = f"Request failed with status code {response.status_code}: {response.reason}"
                            await message.answer(f"Error---{result}")

                    except requests.exceptions.RequestException as e:
                        result = f"Request failed: {e}"
                        await message.answer(f"Error---{result}")
                    await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                    await state.finish()





                    a = start_t + 'T00:00:00'
                    f = message.text + 'T00:00:00'
                    start = datetime.strptime(a, "%Y-%m-%dT%H:%M:%S")
                    finish = datetime.strptime(f, "%Y-%m-%dT%H:%M:%S")
                    start_formatted = start.strftime("%Y-%m-%d %H:%M:%S")
                    finish_formatted = finish.strftime("%Y-%m-%d %H:%M:%S")
                    chat_id = message.from_user.id
                    params = {
                    "type": "reconciliation_act",
                        "chat_id": chat_id,
                        "start":start_formatted,
                        "finish":finish_formatted
                }
                headers = {
                    'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
                    'User-Agent': 'PostmanRuntime/7.35.0',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                try:
                    response = requests.get(api_url, params=params, headers=headers)
                    if response.ok:
                        if 'application/json' in response.headers.get('Content-Type', ''):
                            data = response.json()
                            print("Mana", data)
                            for key, value in data.items():
                                if data['allsumm'] == None:
                                    await message.answer("You have not debt ")
                                else:
                                    await message.answer(f"{data['allsumm']}----{data['contracts']}")
                            result = response.text
                        else:
                            result = f"Response is not in JSON format: {response.text}"
                            await message.answer(f"Error {result}")
                    else:
                        result = f"Request failed with status code {response.status_code}: {response.reason}"
                        await message.answer(f"Error {result}")

                except requests.exceptions.RequestException as e:
                    result = f"Request failed: {e}"
                    await message.answer(f"Error {result}")
                await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                await state.finish()
                    
            else:
                await message.answer("Enter data in irregular format (chch:mm): ")











if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)