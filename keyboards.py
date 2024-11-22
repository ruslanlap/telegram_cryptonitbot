# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    encrypt_button = KeyboardButton("/encrypt🔒")
    decrypt_button = KeyboardButton("/decrypt🔓")
    help_button = KeyboardButton("/startℹ️")
    markup.add(encrypt_button, decrypt_button, help_button)
    return markup
