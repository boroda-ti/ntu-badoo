from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


reg_button = KeyboardButton("Розпочати реєстрацію")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(reg_button)