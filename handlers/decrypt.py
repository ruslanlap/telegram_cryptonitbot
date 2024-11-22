# handlers/decrypt.py
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from states import DecryptStates
from keyboards import create_main_menu
from utils.encryption import decrypt, escape_markdown_v2
from utils.s3_upload import upload_file_to_s3, get_presigned_url
from utils.language import get_user_language, get_message
import io
import logging

logger = logging.getLogger(__name__)
MAX_MESSAGE_LENGTH = 250

async def decrypt_command(message: types.Message):
   user_lang = await get_user_language(message.from_user.id)
   await message.reply(get_message('enter_password_decrypt', user_lang))
   await DecryptStates.waiting_for_password.set()

async def get_password_for_decryption(message: types.Message, state: FSMContext):
   user_lang = await get_user_language(message.from_user.id)
   password = message.text.strip()

   if not password:
       await message.reply(get_message('empty_password', user_lang))
       return

   await state.update_data(password=password)
   await message.reply(
       get_message('enter_encrypted_message', user_lang, max_length=MAX_MESSAGE_LENGTH)
   )
   await DecryptStates.waiting_for_encrypted_message.set()

async def decrypt_message_handler(message: types.Message, state: FSMContext):
   user_lang = await get_user_language(message.from_user.id)
   encrypted_text = message.text.strip()

   if len(encrypted_text) > MAX_MESSAGE_LENGTH:
       await message.reply(
           get_message('message_too_long', user_lang, max_length=MAX_MESSAGE_LENGTH)
       )
       return

   data = await state.get_data()
   password = data.get('password')

   try:
       decrypted_text = decrypt(encrypted_text, password)
       escaped_message = escape_markdown_v2(decrypted_text)
       response = get_message('decrypted_message', user_lang, message=escaped_message)
       await message.reply(response, parse_mode='MarkdownV2', reply_markup=create_main_menu())

       file_content = f"Password: {password}\n\nDecrypted Message:\n{decrypted_text}\n\n"

       from config import AWS_S3_BUCKET, s3_client
       s3_key = f"decrypted_messages/{message.from_user.id}/{message.message_id}_Decrypted_Message.txt"
       file_url = upload_file_to_s3(s3_client, AWS_S3_BUCKET, s3_key, file_content)

       if file_url:
           # Відправка документа із зашифрованим повідомленням
           caption = get_message('cloud_storage_success', user_lang, type='decrypted')
           await message.reply_document(
               types.InputFile(io.BytesIO(file_content.encode('utf-8')), filename="Decrypted_Message.txt"),
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
   except ValueError as e:
       logger.error(f"Error during decryption: {e}")
       escaped_error = escape_markdown_v2(str(e))
       await message.reply(
           get_message('decryption_error', user_lang, error=escaped_error),
           reply_markup=create_main_menu()
       )

   await state.finish()

def register_decrypt_handlers(dp: Dispatcher):
   dp.register_message_handler(decrypt_command, commands=['decrypt'], state='*')
   dp.register_message_handler(
       decrypt_command,
       lambda message: message.text.lower() in ['d', '/d', '/decrypt🔓', 'decrypt🔓'],
       state='*'
   )
   dp.register_message_handler(
       get_password_for_decryption,
       state=DecryptStates.waiting_for_password,
       content_types=types.ContentTypes.TEXT
   )
   dp.register_message_handler(
       decrypt_message_handler,
       state=DecryptStates.waiting_for_encrypted_message,
       content_types=types.ContentTypes.TEXT
   )