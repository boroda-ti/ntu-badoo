from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def create_keyboard() -> ReplyKeyboardMarkup:
    kb_client = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "Розпочати реєстрацію")]], resize_keyboard=True)
    return kb_client

def create_sex_keyboard() -> ReplyKeyboardMarkup:
    kb_client = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "Чоловік"), KeyboardButton(text = "Жінка")], [KeyboardButton(text = "Інше")]], resize_keyboard=True)
    return kb_client

def delete_keyboard() -> ReplyKeyboardRemove:
    kb_client = ReplyKeyboardRemove()
    return kb_client