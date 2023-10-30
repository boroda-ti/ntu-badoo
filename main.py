import asyncio
import logging

from minio import Minio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import *
from handlers.user.handlers import router, reg_router, bot

from db.postgresql.db import async_session_maker

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.include_router(reg_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), session_maker=async_session_maker)


def main_minio():

    client = Minio(
        MINIO_ENDPOINT,
        MINIO_ACCESS,
        MINIO_SECRET,
        secure=False
    )

    print(client.bucket_exists('avatars'))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main_minio()
    asyncio.run(main())