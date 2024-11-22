import json
import os

DEFAULT_LANGUAGE = 'en'
MESSAGES = {
    'en': {
        'welcome': "👋 Hello, {name}! I'm a bot for encryption/decryption. Use the commands below or shortcuts:\n\n"
                  "🔒 /encrypt or /e - Encrypt message\n"
                  "🔓 /decrypt or /d - Decrypt message\n"
                  "ℹ️ /start or /help - Get help\n"
                  "👋 /hello - Welcome message\n"
                  "🌐 /language - Change language\n\n"
                  "Remember that your password security is very important! Never share your password with others.",
        'enter_password_encrypt': "🔒 Please enter the password for encryption:",
        'enter_password_decrypt': "🔓 Please enter the password for decryption:",
        'empty_password': "⚠️ Password cannot be empty. Please try again:",
        'enter_message': "📧 Please send the message to encrypt (up to {max_length} characters):",
        'enter_encrypted_message': "📧 Please send the encrypted message to decrypt (up to {max_length} characters):",
        'message_too_long': "⚠️ Message is too long. Please limit it to {max_length} characters.",
        'encrypted_message': "🔐 Encrypted message:\n{message}",
        'decrypted_message': "🔓 Decrypted message:\n||{message}||",
        'cloud_storage_error': "⚠️ An error occurred while saving the file to cloud storage.",
        'cloud_storage_success': "🔐 Your {type} message and instructions have been saved in cloud storage.",
        'decryption_error': "⚠️ Decryption error: {error}. Please make sure you entered the correct password and that the message is properly encrypted.",
        'unknown_command': "⚠️ Unknown command. Please use the menu buttons or type /help for assistance.",
        'select_language': "🌐 Please select your language:",
        'language_changed': "✅ Language has been changed to English"
    },
    'uk': {
        'welcome': "👋 Вітаю, {name}! Я бот для шифрування/дешифрування. Використовуйте команди нижче або скорочення:\n\n"
                  "🔒 /encrypt або /e - Шифрувати повідомлення\n"
                  "🔓 /decrypt або /d - Дешифрувати повідомлення\n"
                  "ℹ️ /start або /help - Отримати допомогу\n"
                  "👋 /hello - Привітальне повідомлення\n"
                  "🌐 /language - Змінити мову\n\n"
                  "Не забудьте, що безпека вашого паролю дуже важлива! Ніколи не діліться своїм паролем з іншими людьми.",
        'enter_password_encrypt': "🔒 Будь ласка, введіть пароль для шифрування:",
        'enter_password_decrypt': "🔓 Будь ласка, введіть пароль для розшифрування:",
        'empty_password': "⚠️ Пароль не може бути порожнім. Спробуйте ще раз:",
        'enter_message': "📧 Будь ласка, відправте повідомлення для шифрування (до {max_length} символів):",
        'enter_encrypted_message': "📧 Будь ласка, надішліть зашифроване повідомлення для розшифрування (до {max_length} символів):",
        'message_too_long': "⚠️ Повідомлення занадто довге. Будь ласка, обмежте його до {max_length} символів.",
        'encrypted_message': "🔐 Зашифроване повідомлення:\n{message}",
        'decrypted_message': "🔓 Розшифроване повідомлення:\n||{message}||",
        'cloud_storage_error': "⚠️ Сталася помилка під час збереження файлу в хмарному сховищі.",
        'cloud_storage_success': "🔐 Ваше {type} повідомлення та інструкції збережені в хмарному сховищі.",
        'decryption_error': "⚠️ Помилка розшифрування: {error}. Будь ласка, переконайтеся, що ви ввели правильний пароль і що повідомлення правильно зашифроване.",
        'unknown_command': "⚠️ Невідома команда. Будь ласка, використовуйте кнопки меню або введіть /help для отримання допомоги.",
        'select_language': "🌐 Будь ласка, оберіть мову:",
        'language_changed': "✅ Мову змінено на українську"
    }
}

async def get_user_language(user_id: int) -> str:
    try:
        with open('utils/user_languages.json', 'r') as f:
            languages = json.load(f)
            return languages.get(str(user_id), DEFAULT_LANGUAGE)
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_LANGUAGE

async def set_user_language(user_id: int, language: str) -> None:
    os.makedirs('utils', exist_ok=True)
    try:
        with open('utils/user_languages.json', 'r') as f:
            languages = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        languages = {}

    languages[str(user_id)] = language

    with open('utils/user_languages.json', 'w') as f:
        json.dump(languages, f)

def get_message(key: str, lang: str = 'en', **kwargs) -> str:
    """
    Get a localized message with formatting.

    Args:
        key (str): The message key to look up
        lang (str): Language code ('en' or 'uk')
        **kwargs: Format arguments for the message string

    Returns:
        str: The formatted message in the requested language
    """
    default_lang = 'en'

    try:
        # First try to get the message in the requested language
        messages_for_lang = MESSAGES.get(lang, MESSAGES[default_lang])
        message = messages_for_lang.get(key)

        # If not found, fall back to default language
        if message is None:
            message = MESSAGES[default_lang].get(key)

        # If still not found, return error message
        if message is None:
            return f"Message not found: {key}"

        # Try to format the message with the provided arguments
        try:
            return message.format(**kwargs)
        except KeyError as e:
            return f"Missing format argument: {e}"
        except ValueError as e:
            return f"Invalid format string: {e}"

    except Exception as e:
        return f"Error processing message: {e}"