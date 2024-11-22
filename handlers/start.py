# handlers/start.py
from aiogram import types, Dispatcher
from keyboards import create_main_menu

async def send_welcome(message: types.Message):
    response = (
        f"👋 Вітаю, {message.from_user.first_name}! Я бот для шифрування/дешифрування. Використовуйте команди нижче або скорочення:\n\n"
        "🔒 /encrypt або /e - Шифрувати повідомлення\n"
        "🔓 /decrypt або /d - Дешифрувати повідомлення\n"
        "ℹ️ /start або /help - Отримати допомогу\n"
        "👋 /hello - Привітальне повідомлення\n\n"
        "Не забудьте, що безпека вашого паролю дуже важлива! Ніколи не діліться своїм паролем з іншими людьми."
    )
    await message.reply(response, reply_markup=create_main_menu())

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help', 'startℹ️'])
