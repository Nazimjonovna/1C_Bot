import logging
from aiogram import Bot, Dispatcher, executor, types
from buttons import *
import requests
import json

# Your API endpoint URL
api_url = 'http://192.168.100.49:8000/telegram/hs/hl/gd'

# Token of tg_Bot
API_TOKEN = '6619844226:AAGpUYECES7ReYNnSVZdWMYV8yhhtdcGEfk'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Tilni tanlang\n\nВыберите язык\n\nSelect language", reply_markup=lang)


@dp.message_handler(text = "🇺🇿")
async def uzb(message: types.Message):
    await message.answer("Assalomu alaykum, OOO APPLOAD CRM botiga xush kelibsiz!\nIdentifikatsiyadan o’tish uchun telefon raqamingizni ulashing.", reply_markup=contact_uz)



    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def uzb_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = message.contact.phone_number
        chat_id = message.from_user.id
        print("you are", chat_id)
        payload = {
            "type": "phone",
            "chat_id": chat_id,
            "phone_number": phone_number
        }
        payload_json = json.dumps(payload)

        try:
            response = requests.post(api_url, data=payload_json, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                print("Data sent successfully to the API")
            else:
                print("Failed to send data to the API")
            await message.answer(f"Mijoz : {message.contact.full_name}\nTelefon: {message.contact.phone_number}",
                                 reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            print("Request Exception:", e)
            print("Failed to connect to the API. Check the URL or network connection.")

    # async def uzb_baza(message: types.Message):
    #     global phone_number, chat_id
    #     phone_number = message.contact.phone_number
    #     chat_id = message.from_user.id
    #     payload = {
    #         "type": "phone",
    #         "chat_id": chat_id,
    #         "phone_number": phone_number
    #     }
    #     payload_json = json.dumps(payload)
    #     response = requests.post(api_url, data=payload_json, headers={'Content-Type': 'application/json'})
    #     if response.status_code == 200:
    #         print("Data sent successfully to the API")
    #     else:
    #         print("Failed to send data to the API")
    #     await message.answer(f"Mijoz : {message.contact.full_name}\nTelefon: {message.contact.phone_number}",
    #                          reply_markup=user_uz)



        @dp.message_handler(text = 'Qarzdorlikni tekshirish ＄')
        async def uzb_baz(message: types.Message):
            await message.answer(f"Quyidagi bo'limlardan birini tanlang: ",reply_markup=c_button_uz)

            @dp.message_handler(text = 'AllSumm')
            async def all(message: types.Message):
                # dbdan kelgan ma'lumotni filterlash kk'
                await message.reply("Sizning qarzdorligingiz")

        @dp.message_handler(text = 'Biz bilan bog’lanish 📞')
        async def admin(message: types.Message):
            await message.answer("Admin: @pm_hilol")

        @dp.message_handler(text='Akt sverka olish 🧾')
        async def admin(message: types.Message):
            await message.answer("Qaysi shartnoma bo’yicha akt sverka olmoqchisiz", reply_markup=akt_button)

            @dp.callback_query_handlers(data = "1")
            async def akt(message: types.Message):
                await message.answer("Boshlanish sanasini tanlang: ")
                await message.answer("Tugatish sanasini tanlang: ")

        # @dp.message_handler()
        # async def buton(message: types.Message):
            # print('q')
            # m = message.text
            #
            #     # Split the message into words or items to determine the number of buttons
            # items = m.split()
            # print(items)# Split the message by spaces, you can adjust this based on your message format
            #
            # keyboard_buttons = [
            #     [InlineKeyboardButton(f"{item}", callback_data=f"{item}")]
            #     for item in items
            # ]
           #      m = message.text
           #      print(m)
           #      keyboard_buttons = [
           #     for i in range(int(m)):
           #          [InlineKeyboardButton(f"{i}", callback_data=f"{i}")]
           # ]




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