from aiogram import F, Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.enums import ContentType
from aiogram.enums.parse_mode import ParseMode

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import *
from middlewares.register_check import Register_Check
from keyboards.reply import *

from db.mongodb.db import *
from main_minio.main import *

import os
import random

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

AVAILABLE_TAGS = ['спорт', 'кіберспорт', 'ігри', 'музика', 'фільми', 'серіали', 'література', 'книжки', 'аніме', 'манга', 'технології', 
                  'програмування', "кар'єра", 'наука', 'фітнес', 'відпочинок', 'подорожі', 'волонтер', 'дизайн', 'творчість', 'мови', 
                  'феминизм', 'історія', 'саморозвиток', 'архітектура', 'гроші', 'заробіток', 'політика', 'економіка']

STRING_TAGS = ' '.join(tag for tag in AVAILABLE_TAGS)

class Form(StatesGroup):
    username = State()
    age = State()
    sex = State()
    about = State()
    tags = State()
    img_name = State()

class EditForm(StatesGroup):
    method = State()
    data = State()

class SearchForm(StatesGroup):
    method = State()
    forms = State()

class SearchByTagForm(StatesGroup):
    method = State()
    forms = State()

router = Router()

reg_router = Router()
reg_router.message.middleware(Register_Check())

@reg_router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer('Вітаємо тебе в чат-боті для знайомств! Бажаєш знайти однодумців, чи, можливо, просто спілкування? Хутчіш створюй анкету та починай пошук!', reply_markup=create_keyboard())

@router.message(lambda msg: msg.text.lower() == 'подивитися свою анкету')
async def profile_handler(msg: Message):
    data = get_form(msg.from_user.id)
    minio_client = create_connection()
    get_photo(minio_client, f'media/temp/{data["user_id"]}.jpg', f'{data["user_id"]}.jpg')

    tags = ' '.join(tag for tag in data['tags'])
    text = f'{data["username"]} {data["age"]} років\n{data["about"]}\nМої теги: {tags}\n{data["sex"]}'
    await msg.answer_photo(photo=FSInputFile(path=f'media/temp/{data["user_id"]}.jpg'), caption=text, reply_markup=profile_keyboard())

    os.remove(f'media/temp/{data["user_id"]}.jpg')

@router.message(lambda msg: msg.text.lower() in ["редагувати ім'я", "редагувати вік", "редагувати стать", "редагувати біографію", "редагувати теги"])
async def choose_method_edit_handler(msg: Message, state: FSMContext):
    await state.set_state(EditForm)
    await state.update_data(method=msg.text.lower())
    match msg.text.lower():
        case "редагувати ім'я":
            await msg.answer("Введи своє ім'я", reply_markup=delete_keyboard())
        case "редагувати вік":
            await msg.answer("Введи свій вік", reply_markup=delete_keyboard())
        case "редагувати стать":
            await msg.answer("Обери свою стать", reply_markup=create_sex_keyboard())
        case "редагувати біографію":
            await msg.answer("Заповни свою біографію, або напиши пусто, якщо бажаєш залишити поле біографії пустим", reply_markup=delete_keyboard())
        case "редагувати теги":
            await msg.answer(f"Список тегів: {STRING_TAGS}.")
            await msg.answer("Вибери теги - це твої захоплення. Формат відправки теги з списку через пробіл: 'ігри фільми готувати', або напиши пусто, якщо бажаєш залишити поле тегів пустим.", reply_markup=delete_keyboard())

    await state.set_state(EditForm.data)


@router.message(lambda msg: msg.text.lower() in ['розпочати реєстрацію', 'створити заново'])
async def start_reg_handler(msg: Message, state: FSMContext):
    await msg.answer("Щоб припинити заповнення анкети просто напиши відхилити або /cancel")
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
            await msg.answer("Введи свій вік знову")
            return
    except (TypeError, ValueError):
        await msg.answer("Введи вік числом")
        await msg.answer("Введи свій вік знову")
        return

    await state.update_data(age=int(msg.text))
    await msg.answer("Обери свою стать", reply_markup=create_sex_keyboard())
    await state.set_state(Form.sex)

@router.message(Form.sex)
async def process_sex(msg: Message, state: FSMContext):
    if msg.text not in ['Чоловік', 'Жінка', 'Інше']:
        await msg.answer("Ви ввели невірну стать, виберіть з запропонованих")
        await msg.answer("Обери свою стать", reply_markup=create_sex_keyboard())
        return

    await state.update_data(sex=msg.text)
    await msg.answer("Додай опис до своєї анкети, або напиши пусто, якщо бажаєш залишити поле біографії пустим", reply_markup=delete_keyboard())
    await state.set_state(Form.about)

@router.message(Form.about)
async def process_about(msg: Message, state: FSMContext):
    if msg.text.lower() == 'пусто':
        await state.update_data(about='')
    else:
        await state.update_data(about=msg.text.lower())

    await msg.answer(f"Список тегів: {STRING_TAGS}.")
    await msg.answer("Вибери теги - це твої захоплення. Формат відправки теги з списку через пробіл: 'ігри фільми готувати', або напиши пусто, якщо бажаєш залишити поле тегів пустим.")
    await state.set_state(Form.tags)

@router.message(Form.tags)
async def process_tags(msg: Message, state: FSMContext):
    if msg.text.lower() == 'пусто':
        await state.update_data(tags=[])
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

    if form_exists(result['user_id']):
        await msg.answer('В тебе вже є анкета. Бажаєш змінити данні анкети на нові?', reply_markup=yes_no_keyboard())
    else:
        send_mongodb(result)

        minio_client = create_connection()

        img = await bot.get_file(msg.photo[-1].file_id)
        img_path = img.file_path

        await bot.download_file(img_path, f'media/temp/{msg.from_user.id}.jpg')
        send_photo(minio_client, f'media/temp/{msg.from_user.id}.jpg', f'{msg.from_user.id}.jpg')
        os.remove(f'media/temp/{msg.from_user.id}.jpg')
    
        await msg.answer('Анкета заповнена!', reply_markup=main())

    await state.clear()

@router.message(lambda msg: msg.text.lower() in ['змінити анкету', 'відхилити зміни'])
async def process_change(msg: Message, state: FSMContext):
    if msg.text.lower() == 'змінити анкету':
        data = await state.get_data()
        update_form(msg.from_user.id, data)
        await msg.answer("Ваша анкета успішно оновлена!", reply_markup=main())
    elif msg.text.lower() == 'відхилити зміни':
        await state.clear()
        await msg.answer(text="Створення анкети відхилено", reply_markup=main())
    else:
        await msg.answer("Щось не зрозуміле...", reply_markup=delete_keyboard())
        return

@router.message(Command('cancel'))
@router.message(F.text.lower() == "відхилити")
async def cmd_cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(text="Створення анкети відхилено", reply_markup=main())



@router.message(Command('search'))
@router.message(lambda msg: msg.text.lower() in ['почати пошук', 'пошук'])
async def process_search(msg: Message, state: FSMContext):
    data = get_all_forms(f'{msg.from_user.id}')
    await state.set_state(SearchByTagForm) # new

    if data == []:
        await msg.answer('На жаль немає вільних анкет', reply_markup=main())
        await state.clear()
        return

    form = data.pop(random.randint(0, len(data)-1))
    await state.update_data(forms=data)

    # form = data.pop()
    # await state.update_data(forms=data)

    minio_client = create_connection()
    get_photo(minio_client, f'media/temp/{form["user_id"]}.jpg', f'{form["user_id"]}.jpg')

    tags = ' '.join(tag for tag in form['tags'])
    text = f'{form["username"]} {form["age"]} років\n{form["about"]}\nМої теги: {tags}\n{form["sex"]}'
    await msg.answer_photo(photo=FSInputFile(path=f'media/temp/{form["user_id"]}.jpg'), caption=text, reply_markup=search_keyboard())

    os.remove(f'media/temp/{form["user_id"]}.jpg')

    await state.set_state(SearchForm.method)

@router.message(SearchForm.method)
async def process_next_or_cancel_search(msg: Message, state: FSMContext):
    data = await state.get_data()
    try:
        forms = data['forms']
    except:
        await msg.answer('На жаль немає вільних анкет.', reply_markup=main())
        await state.clear()
        return

    if msg.text.lower() == 'закінчити пошук':
        await msg.answer('Пошук закінчен.', reply_markup=main())
        await state.clear()
        return # new
    elif forms == []:
        await msg.answer('На жаль немає вільних анкет', reply_markup=main())
        await state.clear()
        return # new
    elif msg.text.lower() == 'шукати далі':
        form = forms.pop(random.randint(0, len(data)-1))
        await state.update_data(forms=forms)

        # form = forms.pop()
        # await state.update_data(forms=forms)

        minio_client = create_connection()
        get_photo(minio_client, f'media/temp/{form["user_id"]}.jpg', f'{form["user_id"]}.jpg')

        tags = ' '.join(tag for tag in form['tags'])
        text = f'{form["username"]} {form["age"]} років\n{form["about"]}\nМої теги: {tags}\n{form["sex"]}'
        await msg.answer_photo(photo=FSInputFile(path=f'media/temp/{form["user_id"]}.jpg'), caption=text, reply_markup=search_keyboard())

        os.remove(f'media/temp/{form["user_id"]}.jpg')
    else:
        await msg.answer('Щось не зрозуміле...', reply_markup=delete_keyboard())
        await state.clear()
        return # new

    await state.set_state(SearchForm.method)



@router.message(Command('search_by_tag'))
@router.message(lambda msg: msg.text.lower() in ['почати пошук за тегами', 'пошук за тегами'])
async def process_search_by_tag(msg: Message, state: FSMContext):
    data = get_forms_by_tags(f'{msg.from_user.id}')
    await state.set_state(SearchByTagForm) # new

    if data == []:
        await msg.answer('На жаль немає анкет з спільними тегами', reply_markup=main())
        await state.clear()
        return

    form = data.pop(random.randint(0, len(data)-1))
    await state.update_data(forms=data)

    # form = data.pop()
    # await state.update_data(forms=data)

    minio_client = create_connection()
    get_photo(minio_client, f'media/temp/{form["user_id"]}.jpg', f'{form["user_id"]}.jpg')

    tags = ' '.join(tag for tag in form['tags'])
    text = f'{form["username"]} {form["age"]} років\n{form["about"]}\nМої теги: {tags}\n{form["sex"]}'
    await msg.answer_photo(photo=FSInputFile(path=f'media/temp/{form["user_id"]}.jpg'), caption=text, reply_markup=search_keyboard())

    os.remove(f'media/temp/{form["user_id"]}.jpg')

    await state.set_state(SearchByTagForm.method)

@router.message(SearchByTagForm.method)
async def process_next_or_cancel_search_by_tag(msg: Message, state: FSMContext):
    data = await state.get_data()
    try:
        forms = data['forms']
    except:
        await msg.answer('На жаль немає анкет з спільними тегами', reply_markup=main())
        await state.clear()
        return

    if msg.text.lower() == 'закінчити пошук':
        await msg.answer('Пошук закінчен.', reply_markup=main())
        await state.clear()
        return
    elif forms == []:
        await msg.answer('На жаль немає анкет з спільними тегами', reply_markup=main())
        await state.clear()
        return
    elif msg.text.lower() == 'шукати далі':
        form = forms.pop(random.randint(0, len(data)-1))
        await state.update_data(forms=forms)

        # form = forms.pop()
        # await state.update_data(forms=forms)

        minio_client = create_connection()
        get_photo(minio_client, f'media/temp/{form["user_id"]}.jpg', f'{form["user_id"]}.jpg')

        tags = ' '.join(tag for tag in form['tags'])
        text = f'{form["username"]} {form["age"]} років\n{form["about"]}\nМої теги: {tags}\n{form["sex"]}'
        await msg.answer_photo(photo=FSInputFile(path=f'media/temp/{form["user_id"]}.jpg'), caption=text, reply_markup=search_keyboard())

        os.remove(f'media/temp/{form["user_id"]}.jpg')
    else:
        await msg.answer('Щось не зрозуміле...', reply_markup=delete_keyboard())
        await state.clear()

    await state.set_state(SearchByTagForm.method)