# handlers/hello.py
from aiogram import types, Dispatcher
from keyboards import create_main_menu

async def hello_command(message: types.Message):
    response = (
        f"Привіт, {message.from_user.first_name}! 👋\n"
        "Я допоможу тобі шифрувати або дешифрувати повідомлення. Для отримання допомоги введіть команду /help або /start."
    )
    await message.reply(response, reply_markup=create_main_menu())

def register_hello_handlers(dp: Dispatcher):
    dp.register_message_handler(hello_command, commands=['hello'])
