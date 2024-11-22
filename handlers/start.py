# handlers/start.py
from aiogram import types, Dispatcher
from keyboards import create_main_menu
from utils.language import get_user_language, get_message

async def send_welcome(message: types.Message):
    user_lang = await get_user_language(message.from_user.id)
    response = get_message('welcome', user_lang, name=message.from_user.first_name)
    await message.reply(response, reply_markup=create_main_menu())

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help', 'startℹ️'])