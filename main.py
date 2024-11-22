# main.py
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET
import boto3
from handlers import register_handlers

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація S3 клієнта
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Додавання S3 клієнта до об'єкта диспетчера для доступу в обробниках
dp.bot['s3_client'] = s3_client
dp.bot['aws_s3_bucket'] = AWS_S3_BUCKET

# Реєстрація всіх обробників
register_handlers(dp)

# Обробник невідомих команд
@dp.message_handler()
async def unknown_command(message: types.Message):
    from keyboards import create_main_menu
    await message.reply("⚠️ Невідома команда. Будь ласка, використовуйте кнопки меню або введіть /help для отримання допомоги.", reply_markup=create_main_menu())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
