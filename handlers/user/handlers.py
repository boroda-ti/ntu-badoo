from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards.reply import create_keyboard

router = Router()

@router.message(Command('start'))
async def start_handler(msg: Message):
    keyboard = create_keyboard()
    await msg.answer('Text', reply_markup=keyboard)