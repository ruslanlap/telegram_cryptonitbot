# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton('/encrypt 🔒'),
        KeyboardButton('/decrypt 🔓')
    )
    keyboard.add(
        KeyboardButton('/start ℹ️'),
        KeyboardButton('/language 🌐')
    )
    return keyboard
