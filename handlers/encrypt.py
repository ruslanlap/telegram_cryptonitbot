# handlers/encrypt.py

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from states import EncryptStates
from keyboards import create_main_menu
from utils.language import get_user_language, get_message
from utils.encryption import encrypt, escape_markdown_v2
from utils.s3_upload import upload_file_to_s3
import os
import io

MAX_MESSAGE_LENGTH = 250

async def encrypt_command(message: types.Message):
    user_lang = await get_user_language(message.from_user.id)
    await message.reply(get_message('enter_password_encrypt', user_lang))
    await EncryptStates.waiting_for_password.set()

async def get_password_for_encryption(message: types.Message, state: FSMContext):
    user_lang = await get_user_language(message.from_user.id)
    password = message.text.strip()
    if not password:
        await message.reply(get_message('empty_password', user_lang))
        return

    await state.update_data(password=password)
    await message.reply(
        get_message('enter_message', user_lang, max_length=MAX_MESSAGE_LENGTH)
    )
    await EncryptStates.waiting_for_message.set()

async def encrypt_message_handler(message: types.Message, state: FSMContext):
    user_lang = await get_user_language(message.from_user.id)
    text = message.text.strip()
    if len(text) > MAX_MESSAGE_LENGTH:
        await message.reply(
            get_message('message_too_long', user_lang, max_length=MAX_MESSAGE_LENGTH)
        )
        return

    data = await state.get_data()
    password = data.get('password')
    encrypted = encrypt(text, password)
    escaped_encrypted = escape_markdown_v2(encrypted)
    response = get_message('encrypted_message', user_lang, message=escaped_encrypted)
    await message.reply(response, parse_mode='MarkdownV2', reply_markup=create_main_menu())

    file_content = f"Password: {password}\n\nEncrypted Message:\n{encrypted}\n\n"

    instruction_file = f"Instructions_{user_lang}.txt"
    if os.path.exists(instruction_file):
        with open(instruction_file, 'r', encoding='utf-8') as instructions_file:
            file_content += instructions_file.read()

    from config import AWS_S3_BUCKET, s3_client
    s3_key = f"encrypted_messages/{message.from_user.id}/{message.message_id}_Encrypted_Message.txt"
    file_url = upload_file_to_s3(s3_client, AWS_S3_BUCKET, s3_key, file_content)

    if file_url:
       # Відправка документа без URL
       caption = get_message('cloud_storage_success', user_lang, type='encrypted')
       await message.reply_document(
           types.InputFile(io.BytesIO(file_content.encode('utf-8')), filename="Encrypted_Message.txt"),
           caption=caption
       )
       # Відправка URL окремим повідомленням
       cloud_message = ("🔓 Ваше розшифроване повідомлення та інструкції також збережені в хмарному сховищі." 
                       if user_lang == 'uk' else 
                       "🔓 Your decrypted message and instructions are also stored in cloud storage.")
       await message.reply(
           f"{cloud_message}\n{file_url}"
       )
    else:
       await message.reply(
           get_message('cloud_storage_error', user_lang),
           reply_markup=create_main_menu()
       )
    await state.finish()

def register_encrypt_handlers(dp: Dispatcher):
    dp.register_message_handler(encrypt_command, commands=['encrypt'], state='*')
    dp.register_message_handler(encrypt_command, lambda message: message.text in ['e', '/e', '/encrypt🔒', 'encrypt🔒'], state='*')
    dp.register_message_handler(get_password_for_encryption, state=EncryptStates.waiting_for_password)
    dp.register_message_handler(encrypt_message_handler, state=EncryptStates.waiting_for_message)