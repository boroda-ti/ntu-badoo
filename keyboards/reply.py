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

def search_keyboard() -> ReplyKeyboardMarkup:
    kb_client = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "Шукати далі"), KeyboardButton(text = "Закінчити пошук")]], resize_keyboard=True)
    return kb_client

def yes_no_keyboard() -> ReplyKeyboardMarkup:
    kb_client = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "Змінити анкету"), KeyboardButton(text = "Відхилити зміни")]], resize_keyboard=True)
    return kb_client

def main() -> ReplyKeyboardMarkup:
    kb_client = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "Пошук"), KeyboardButton(text = "Пошук за тегами")], [KeyboardButton(text = "Подивитися свою анкету")]], resize_keyboard=True)
    return kb_client

def profile_keyboard() -> ReplyKeyboardMarkup:
    kb_client = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "Редагувати ім'я"), KeyboardButton(text = "Редагувати вік"), KeyboardButton(text = "Редагувати стать")],
                                              [KeyboardButton(text = "Редагувати біографію"), KeyboardButton(text = "Редагувати теги"), KeyboardButton(text = "Редагувати фото")],
                                              [KeyboardButton(text = "Створити заново"), KeyboardButton(text = "Пошук"), KeyboardButton(text = "Пошук за тегами")]], resize_keyboard=True)
    return kb_client