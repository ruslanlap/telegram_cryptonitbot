# handlers/encrypt.py
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from states import EncryptStates
from keyboards import create_main_menu
from utils.encryption import encrypt, escape_markdown_v2
from utils.s3_upload import upload_file_to_s3
import os
import io

MAX_MESSAGE_LENGTH = 250

async def encrypt_command(message: types.Message):
    await message.reply("🔒 Будь ласка, введіть пароль для шифрування:")
    await EncryptStates.waiting_for_password.set()

async def get_password_for_encryption(message: types.Message, state: FSMContext):
    password = message.text.strip()
    if not password:
        await message.reply("⚠️ Пароль не може бути порожнім. Будь ласка, спробуйте ще раз:")
        return
    await state.update_data(password=password)
    await message.reply(f"📧 Будь ласка, відправте повідомлення для шифрування (до {MAX_MESSAGE_LENGTH} символів):")
    await EncryptStates.waiting_for_message.set()

async def encrypt_message_handler(message: types.Message, state: FSMContext):
    text = message.text.strip()
    if len(text) > MAX_MESSAGE_LENGTH:
        await message.reply(f"⚠️ Повідомлення занадто довге. Будь ласка, обмежте його до {MAX_MESSAGE_LENGTH} символів.")
        return
    data = await state.get_data()
    password = data.get('password')
    encrypted = encrypt(text, password)
    escaped_encrypted = escape_markdown_v2(encrypted)
    response = f"🔐 Зашифроване повідомлення:\n{escaped_encrypted}"
    await message.reply(response, reply_markup=create_main_menu())

    # Відправка зашифрованого повідомлення як документ у хмарному сховищі
    file_content = f"Password: {password}\n\nEncrypted Message:\n{encrypted}\n\n"
    # Додавання інструкцій, якщо файл існує
    if os.path.exists("Instructions.txt"):
        with open("Instructions.txt", 'r', encoding='utf-8') as instructions_file:
            file_content += instructions_file.read()
    else:
        # Можна використовувати логгер для попередження
        pass

    # Завантаження файлу в S3
    from config import AWS_S3_BUCKET, s3_client  # Імпортуємо необхідні змінні
    s3_key = f"encrypted_messages/{message.from_user.id}/{message.message_id}_Encrypted_Message.txt"
    file_url = upload_file_to_s3(s3_client, AWS_S3_BUCKET, s3_key, file_content)
    if file_url:
        await message.reply_document(
            types.InputFile(io.BytesIO(file_content.encode('utf-8')), filename="Encrypted_Message.txt"),
            caption="🔐 Ваше зашифроване повідомлення та інструкції також збережено у хмарному сховищі."
        )
    else:
        await message.reply("⚠️ Сталася помилка при збереженні файлу у хмарному сховищі.", reply_markup=create_main_menu())

    await state.finish()

def register_encrypt_handlers(dp: Dispatcher):
    dp.register_message_handler(encrypt_command, commands=['encrypt', 'e', 'encrypt🔒'])
    dp.register_message_handler(get_password_for_encryption, state=EncryptStates.waiting_for_password, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(encrypt_message_handler, state=EncryptStates.waiting_for_message, content_types=types.ContentTypes.TEXT)
