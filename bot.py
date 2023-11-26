import logging
from aiogram import Bot, Dispatcher, executor, types
from buttons import *
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import re
import asyncio
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Your API endpoint URL
api_url = 'http://5.182.26.180:55565/telegram/hs/hl/gd'
login = 'HILOL'
password = '0ut0fb0unD'

# Token of tg_Bot
API_TOKEN = telegram_bot_token

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


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Tilni tanlang\n\nВыберите язык\n\nSelect language", reply_markup=lang)


@dp.message_handler(text = "🇺🇿")
async def uzb(message: types.Message):
    await message.answer("Assalomu alaykum, OOO APPLOAD CRM botiga xush kelibsiz!\nIdentifikatsiyadan o’tish uchun telefon raqamingizni ulashing.", reply_markup=contact_uz)



    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def uzb_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = "+998933333349"  #message.contact.phone_number
        chat_id = '901569590'    # message.from_user.id
        params = {
            'type': 'phone',
            'chat_id': 901569590,
            'phone_number': '+998933411945'
        }

        # Headers to send with the request
        headers = {
            'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
            'User-Agent': 'PostmanRuntime/7.35.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        try:
            # Perform the GET request with the specified headers and Basic Authentication
            response = requests.get(api_url, params=params, headers=headers)

            # Check if the request was successful
            if response.ok:
                # Attempt to print the JSON if the content type is correct
                if 'application/json' in response.headers.get('Content-Type', ''):
                    data = response.json()
                    result = response.text
                else:
                    result = f"Response is not in JSON format: {response.text}"
            else:
                # Handle request error
                result = f"Request failed with status code {response.status_code}: {response.reason}"
            await message.answer(f"{data.get('UZ')}", reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            # A serious problem happened, like an SSLError or InvalidURL
            result = f"Request failed: {e}"

            await message.answer(f"{data.get('UZ')}")


        @dp.message_handler(text = 'Qarzdorlikni tekshirish ＄')
        async def uzb_baz(message: types.Message):
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
                        await message.answer(f"Sizdagi xatolik {result}")
                else:
                    result = f"Request failed with status code {response.status_code}: {response.reason}"
                    await message.answer(f"Sizdagi xatolik {result}")

            except requests.exceptions.RequestException as e:
                result = f"Request failed: {e}"
                await message.answer(f"Sizdagi xatolik {result}")
            await message.answer(f"Quyidagi bo'limlardan birini tanlang: ",reply_markup=c_button_uz)

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
                                    await message.answer("Sizda hozircha mablag' yo ")
                                else:
                                    await message.answer(f"{data['allsumm']}----{data['contracts']}")
                            result = response.text
                        else:
                            result = f"Response is not in JSON format: {response.text}"
                            await message.answer(f"Sizdagi xatolik {result}")
                    else:
                        result = f"Request failed with status code {response.status_code}: {response.reason}"
                        await message.answer(f"Sizdagi xatolik {result}")

                except requests.exceptions.RequestException as e:
                    result = f"Request failed: {e}"
                    await message.answer(f"Sizdagi xatolik {result}")

            @dp.message_handler(text = 'Bosh menyuga qaytish 🔙')
            async def back(message: types.Message):
                await message.answer(text = "Orqaga",reply_markup=user_uz)

        @dp.message_handler(text = 'Biz bilan bog’lanish 📞')
        async def admin(message: types.Message):
            await message.answer("Admin: @pm_hilol")

        @dp.message_handler(text='Akt sverka olish 🧾')
        async def start_handler(message: types.Message, state: FSMContext):
            await TimeInput.start_time.set()
            await message.answer("Boshlang'ich sanani kiriting: ")


        @dp.message_handler(state=TimeInput.start_time)
        async def start_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{2}:\d{2}', message.text):
                async with state.proxy() as data:
                    data['start'] = message.text
                    await TimeInput.next()
                    await message.answer("Tugash sanani kiriting: ")
            else:
                await message.answer("Noto'g'ri formatda sanani kiriting (hh:mm): ")


        @dp.message_handler(state=TimeInput.end_time)
        async def end_time_handler(message: types.Message, state: FSMContext):
            if re.match(r'\d{2}:\d{2}', message.text):
                async with state.proxy() as data:
                    data['finish'] = message.text
                    await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                    await state.finish()
            else:
                await message.answer("Noto'g'ri formatda sanani kiriting (hh:mm): ")

        @dp.message_handler(state=TimeInput.end_time)
        async def akt(message: types.Message):
            global start, finish
            chat_id = message.from_user.id
            payload = {
                "type": "reconciliation_act",
                "chat_id": chat_id,
                "start":start,
                "finish":finish
            }
            payload_json = json.dumps(payload)
            try:
                response = requests.get(api_url, data=payload_json, auth=(login, password),
                                        headers={'Content-Type': 'application/json'})
                print(response.status_code)
                print(response.content)

                if response.status_code == 200:
                    print("Data sent successfully to the API")
                    await message.answer("Data sent successfully")
                else:
                    print("Failed to send data to the API")
                    await message.answer("Failed to send data")

                await message.answer(
                    f"Mijoz : {message.contact.full_name}\nTelefon: {message.contact.phone_number}",
                    reply_markup=user_uz)
            except requests.exceptions.RequestException as e:
                print("Request Exception:", e)
                print("Failed to connect to the API. Check the URL or network connection.")
            await message.answer("Qaysi shartnoma bo’yicha akt sverka olmoqchisiz", reply_markup=akt_button)











@dp.message_handler(text = "🇷🇺")
async def ru(message: types.Message):
    await message.answer("Здравствуйте, добро пожаловать в бот ООО «Апплоад CRM»!\nПоделитесь своим номером телефона для аутентификации.", reply_markup=contact_ru)

    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def ru_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = message.contact.phone_number
        chat_id = message.from_user.id
        payload = {
            "type": "phone",
            "chat_id": chat_id,
            "phone_number": phone_number
        }
        payload_json = json.dumps(payload)
        response = requests.post(api_url, data=payload_json, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            print("Data sent successfully to the API")
        else:
            print("Failed to send data to the API")
        await message.answer(f"Клиент : {message.contact.full_name}\nTелефон: {message.contact.phone_number}",
                             reply_markup=user_uz)





        @dp.message_handler(text='Проверка долга ＄')
        async def ru_baz(message: types.Message):
            await message.answer(f"Выберите один из следующих разделов:", reply_markup=c_button_ru)

        @dp.message_handler(text='Связаться с нами 📞')
        async def admin(message: types.Message):
            await message.answer("Admin: @pm_hilol")

        @dp.message_handler(text='Приобретение акта 🧾')
        async def admin(message: types.Message):
            await message.answer("По какому договору вы хотите получить акт-сверку?", reply_markup=akt_button)








@dp.message_handler(text = "🇬🇧")
async def eng(message: types.Message):
    await message.answer("Hello, welcome to OOO APPLOAD CRM bot!\nShare your phone number for authentication.", reply_markup=contact_eng)
    #bazani tekshir
    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def eng_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = message.contact.phone_number
        chat_id = message.from_user.id
        payload = {
            "type": "phone",
            "chat_id": chat_id,
            "phone_number": phone_number
        }
        payload_json = json.dumps(payload)
        response = requests.post(api_url, data=payload_json, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            print("Data sent successfully to the API")
        else:
            print("Failed to send data to the API")
        await message.answer(f"Client : {message.contact.full_name}\nPhone: {message.contact.phone_number}",
                             reply_markup=user_uz)





        @dp.message_handler(text='Debt check ＄')
        async def ru_baz(message: types.Message):
            await message.answer(f"Choose one of the following sections:", reply_markup=c_button_eng)

        @dp.message_handler(text='Contact us 📞')
        async def admin(message: types.Message):
            await message.answer("Admin: @pm_hilol")

        @dp.message_handler(text='Acquiring an act 🧾')
        async def admin(message: types.Message):
            await message.answer("Under which contract do you want to get an act-sverka?", reply_markup=akt_button)










if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)