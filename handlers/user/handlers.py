from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer('Пішов нахуй сука!')
