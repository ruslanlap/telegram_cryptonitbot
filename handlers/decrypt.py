# handlers/decrypt.py
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from states import DecryptStates
from keyboards import create_main_menu
from utils.encryption import decrypt, escape_markdown_v2
from utils.s3_upload import upload_file_to_s3, get_presigned_url  # Updated import
import io

MAX_MESSAGE_LENGTH = 250

# handlers/decrypt.py
# (код залишається без змін)

async def decrypt_command(message: types.Message):
    await message.reply("🔓 Будь ласка, введіть пароль для розшифрування:")
    await DecryptStates.waiting_for_password.set()

async def get_password_for_decryption(message: types.Message, state: FSMContext):
    password = message.text.strip()
    if not password:
        await message.reply("⚠️ Пароль не може бути порожнім. Спробуйте ще раз:")
        return
    await state.update_data(password=password)
    await message.reply(f"📧 Будь ласка, надішліть зашифроване повідомлення для розшифрування (до {MAX_MESSAGE_LENGTH} символів):")
    await DecryptStates.waiting_for_encrypted_message.set()

async def decrypt_message_handler(message: types.Message, state: FSMContext):
    encrypted_text = message.text.strip()
    if len(encrypted_text) > MAX_MESSAGE_LENGTH:
        await message.reply(f"⚠️ Повідомлення занадто довге. Будь ласка, обмежте його до {MAX_MESSAGE_LENGTH} символів.")
        return
    data = await state.get_data()
    password = data.get('password')
    try:
        decrypted_text = decrypt(encrypted_text, password)
        escaped_message = escape_markdown_v2(decrypted_text)
        response = f"🔓 Розшифроване повідомлення:\n||{escaped_message}||"
        await message.reply(response, parse_mode='MarkdownV2', reply_markup=create_main_menu())
        file_content = f"Пароль: {password}\n\nРозшифроване повідомлення:\n{decrypted_text}\n\n"
        from config import AWS_S3_BUCKET, s3_client
        s3_key = f"decrypted_messages/{message.from_user.id}/{message.message_id}_Decrypted_Message.txt"
        file_url = upload_file_to_s3(s3_client, AWS_S3_BUCKET, s3_key, file_content)
        if file_url:
            presigned_url = get_presigned_url(s3_client, AWS_S3_BUCKET, s3_key)
            if presigned_url:
                await message.reply(f"🔗 Посилання на розшифроване повідомлення (дійсне протягом 1 години):\n{presigned_url}", disable_web_page_preview=True)
            await message.reply_document(
                types.InputFile(io.BytesIO(file_content.encode('utf-8')), filename="Decrypted_Message.txt"),
                caption="🔓 Ваше розшифроване повідомлення та інструкції також збережені в хмарному сховищі."
            )
        else:
            await message.reply("⚠️ Сталася помилка під час збереження файлу в хмарному сховищі.", reply_markup=create_main_menu())
    except Exception as e:
        escaped_error = escape_markdown_v2(str(e))
        await message.reply(f"⚠️ Помилка розшифрування: {escaped_error}. Будь ласка, переконайтеся, що ви ввели правильний пароль і що повідомлення правильно зашифроване.", reply_markup=create_main_menu())
    await state.finish()


def register_decrypt_handlers(dp: Dispatcher):
    # Додаємо точну відповідність тексту кнопки
    dp.register_message_handler(
        decrypt_command, 
        lambda message: message.text in ['/decrypt', 'd', '/decrypt🔓', 'decrypt🔓']
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
    dp.register_message_handler(decrypt_command, commands=['decrypt'], state='*')
    dp.register_message_handler(get_password_for_decryption, state=DecryptStates.waiting_for_password)
    dp.register_message_handler(decrypt_message_handler, state=DecryptStates.waiting_for_encrypted_message)