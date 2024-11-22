# handlers/language.py
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.language import get_user_language, set_user_language, get_message
from keyboards import create_main_menu

def register_language_handlers(dp: Dispatcher):
    """Register language handlers"""
    dp.register_message_handler(language_command, commands=['language'])
    dp.register_callback_query_handler(language_callback, lambda c: c.data.startswith('lang_'))

async def language_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("English 🇺🇸", callback_data="lang_en"),
        InlineKeyboardButton("Українська 🇺🇦", callback_data="lang_uk")
    )
    user_lang = await get_user_language(message.from_user.id)
    await message.reply(get_message('select_language', user_lang), reply_markup=keyboard)

async def language_callback(callback_query: types.CallbackQuery):
    lang = callback_query.data.split('_')[1]
    await set_user_language(callback_query.from_user.id, lang)
    await callback_query.message.reply(
        get_message('language_changed', lang),
        reply_markup=create_main_menu()
    )
    await callback_query.answer()