# tests/test_decrypt.py
import pytest
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.utils.exceptions import TelegramAPIError
from handlers.decrypt import register_decrypt_handlers, decrypt_command, get_password_for_decryption, decrypt_message_handler
from states import DecryptStates
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_decrypt_command(dp):
    # Реєстрація обробників
    register_decrypt_handlers(dp)

    # Створення мок повідомлення
    message = AsyncMock(spec=types.Message)
    message.reply = AsyncMock()
    message.text = '/decrypt'

    # Виклик команди
    await decrypt_command(message)

    # Перевірка відповіді
    message.reply.assert_awaited_with("🔓 Будь ласка, введіть пароль для дешифрування:")

@pytest.mark.asyncio
async def test_get_password_for_decryption_valid(dp):
    register_decrypt_handlers(dp)

    message = AsyncMock(spec=types.Message)
    message.reply = AsyncMock()
    message.text = 'valid_password'

    state = AsyncMock()

    await get_password_for_decryption(message, state)

    state.update_data.assert_awaited_with(password='valid_password')
    message.reply.assert_awaited_with(
        "📧 Будь ласка, відправте зашифроване повідомлення для дешифрування (до 250 символів):"
    )

@pytest.mark.asyncio
async def test_get_password_for_decryption_empty(dp):
    register_decrypt_handlers(dp)

    message = AsyncMock(spec=types.Message)
    message.reply = AsyncMock()
    message.text = '   '  # Порожній пароль

    state = AsyncMock()

    await get_password_for_decryption(message, state)

    state.update_data.assert_not_awaited()
    message.reply.assert_awaited_with(
        "⚠️ Пароль не може бути порожнім. Будь ласка, спробуйте ще раз:"
    )

@pytest.mark.asyncio
async def test_decrypt_message_handler_success(dp, mock_upload_file_to_s3, mock_decrypt, mock_escape_markdown_v2):
    register_decrypt_handlers(dp)

    message = AsyncMock(spec=types.Message)
    message.reply = AsyncMock()
    message.reply_document = AsyncMock()
    message.text = 'encrypted_text'
    message.from_user.id = 123456
    message.message_id = 789
    message.reply_document = AsyncMock()

    state = AsyncMock()
    state.get_data = AsyncMock(return_value={'password': 'valid_password'})

    await decrypt_message_handler(message, state)

    # Перевірка виклику функцій
    mock_decrypt.assert_called_with('encrypted_text', 'valid_password')
    mock_escape_markdown_v2.assert_called_with('Decrypted message')
    mock_upload_file_to_s3.assert_called()

    # Перевірка відповідей
    message.reply.assert_any_await(
        "🔓 Розшифроване повідомлення:\n||Decrypted message||",
        parse_mode='MarkdownV2',
        reply_markup=AsyncMock()
    )
    message.reply.assert_any_await(
        "🔗 Посилання на розшифроване повідомлення (дійсне 1 годину):\nhttps://cryptonitbot.s3.amazonaws.com/decrypted_messages/test.txt",
        disable_web_page_preview=True
    )
    message.reply_document.assert_awaited()

@pytest.mark.asyncio
async def test_decrypt_message_handler_encrypted_text_too_long(dp):
    register_decrypt_handlers(dp)

    message = AsyncMock(spec=types.Message)
    message.reply = AsyncMock()
    message.text = 'a' * 251  # Повідомлення довше 250 символів

    state = AsyncMock()

    await decrypt_message_handler(message, state)

    message.reply.assert_awaited_with(
        "⚠️ Повідомлення занадто довге. Будь ласка, обмежте його до 250 символів."
    )

@pytest.mark.asyncio
async def test_decrypt_message_handler_decryption_error(dp, mock_upload_file_to_s3, mock_decrypt, mock_escape_markdown_v2):
    register_decrypt_handlers(dp)

    # Налаштування мок-функцій для генерації помилки
    mock_decrypt.side_effect = Exception("Decryption failed")

    message = AsyncMock(spec=types.Message)
    message.reply = AsyncMock()
    message.text = 'encrypted_text'
    message.from_user.id = 123456
    message.message_id = 789

    state = AsyncMock()
    state.get_data = AsyncMock(return_value={'password': 'invalid_password'})

    await decrypt_message_handler(message, state)

    # Перевірка виклику функцій
    mock_decrypt.assert_called_with('encrypted_text', 'invalid_password')
    mock_escape_markdown_v2.assert_called_with('Decryption failed')

    # Перевірка відповіді з помилкою
    message.reply.assert_awaited_with(
        "⚠️ Помилка дешифрування: Decryption failed. Переконайтеся, що ви ввели правильний пароль і повідомлення зашифроване правильно.",
        reply_markup=AsyncMock()
    )
