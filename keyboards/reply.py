from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_keyboard():
    reg_button = KeyboardButton("Розпочати реєстрацію")
    kb_client = ReplyKeyboardMarkup(keyboard=[[reg_button]], resize_keyboard=True)
    return kb_client