from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ContentType
from aiogram.enums.parse_mode import ParseMode

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import *
from middlewares.register_check import Register_Check
from keyboards.reply import create_keyboard, create_sex_keyboard, delete_keyboard
from db.mongodb.db import send_mongodb

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

AVAILABLE_TAGS = ['спорт', 'кіберспорт', 'ігри', 'музика', 'фільми', 'серіали', 'література', 'книжки', 'аніме', 'манга', 'технології', 
                  'програмування', "кар'єра", 'наука', 'фітнес', 'відпочинок', 'подорожі', 'волонтер', 'дизайн', 'творчість', 'мови', 
                  'феминизм', 'історія', 'саморозвиток', 'архітектура', 'гроші', 'заробіток', 'політика', 'економіка']

URI = f'https://api.telegram.org/file/bot{BOT_TOKEN}/'

class Form(StatesGroup):
    username = State()
    age = State()
    sex = State()
    about = State()
    tags = State()
    img_name = State()

router = Router()

reg_router = Router()
reg_router.message.middleware(Register_Check())

@reg_router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer('Text', reply_markup=create_keyboard())

@router.message(lambda msg: msg.text == 'Розпочати реєстрацію')
async def start_reg_handler(msg: Message, state: FSMContext):
    await msg.answer("Введи своє ім'я", reply_markup=delete_keyboard())
    await state.set_state(Form.username)

@router.message(Form.username)
async def process_name(msg: Message, state: FSMContext):
    await state.update_data(username=msg.text)
    await msg.answer("Тепер введи свій вік")
    await state.set_state(Form.age)

@router.message(Form.age)
async def process_age(msg: Message, state: FSMContext):
    try:
        if int(msg.text) < 16 or int(msg.text) > 50:
            await msg.answer("Твій вік повинен бути від 16 до 50")
            return
    except (TypeError, ValueError):
        await msg.answer("Введи вік числом")
        return

    await state.update_data(age=int(msg.text))
    await msg.answer("Обери свою стать", reply_markup=create_sex_keyboard())
    await state.set_state(Form.sex)

@router.message(Form.sex)
async def process_sex(msg: Message, state: FSMContext):
    if msg.text not in ['Чоловік', 'Жінка', 'Інше']:
        await msg.answer("Ви ввели невірну стать, виберіть з запропонованих")
        return

    await state.update_data(sex=msg.text)
    await msg.answer("Додай опис до своєї анкети, або напиши 'пусто', якщо бажаєш залишити пустим", reply_markup=delete_keyboard())
    await state.set_state(Form.about)

@router.message(Form.about)
async def process_about(msg: Message, state: FSMContext):
    if msg.text.lower() == 'пусто':
        await state.update_data(about='')
    else:
        await state.update_data(about=msg.text.lower())

    await msg.answer("Лист тегів. Вибери теги які стосуються тебе, формат відправки теги з списку через пробіл: 'ігри фільми готувати', або напиши 'пусто', якщо бажаєш залишити пустим")
    await state.set_state(Form.tags)

@router.message(Form.tags)
async def process_tags(msg: Message, state: FSMContext):
    if msg.text.lower() == 'пусто':
        await state.update_data(about=[])
    else:
        tags = msg.text.lower().split(' ')
        valid_tags = [tag for tag in tags if tag in AVAILABLE_TAGS]
        await state.update_data(tags=valid_tags)

    await msg.answer("Останній крок! Надішли мені картинку для своєї анкети.")
    await state.set_state(Form.img_name)

@router.message(Form.img_name)
async def process_img_name(msg: Message, state: FSMContext):
    if msg.content_type != ContentType.PHOTO:
        await msg.answer("Щось не зрозуміле... Надішліть фото для вашої анкети.")
        return
    
    await state.update_data(img_name=f'{msg.from_user.id}.png')  
    data = await state.get_data()

    result = {
        'username' : data['username'], 
        'age' : data['age'], 
        'sex' : data['sex'], 
        'about' : data['about'], 
        'tags' : data['tags'], 
        'img_name' : data['img_name'],
        'user_id': f'{msg.from_user.id}'
    }

    send_mongodb(result)

    img = await bot.get_file(msg.photo[-1].file_id)
    img_path = img.file_path
    fileExt = img.file_path.split(".")[-1]
    await bot.download_file(img_path, f'media/temp/{msg.from_user.id}.{fileExt}')

    await msg.answer('Анкета заповнена!')
    await state.clear()

@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Створення анкети відхилено", reply_markup=delete_keyboard())