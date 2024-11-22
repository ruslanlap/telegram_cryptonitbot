# states.py
from aiogram.dispatcher.filters.state import State, StatesGroup

class EncryptStates(StatesGroup):
    waiting_for_password = State()
    waiting_for_message = State()

class DecryptStates(StatesGroup):
    waiting_for_password = State()
    waiting_for_encrypted_message = State()
