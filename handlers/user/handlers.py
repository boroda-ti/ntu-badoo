from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards.reply import kb_client

router = Router()

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer('Text', reply_markup=kb_client)