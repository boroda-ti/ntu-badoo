from typing import Dict, Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

from sqlalchemy import select

from db.postgresql.models import Users

class Register_Check(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        sessionmaker: sessionmaker = data['session_maker']
        
        async with sessionmaker() as session:
            async with session.begin():
                result = await session.execute(select(Users).where(Users.tg_id == f"{event.from_user.id}"))
                user = result.one_or_none()

                if user:
                    pass
                else:
                    user = Users(
                        tg_id=f"{event.from_user.id}",
                        username=event.from_user.username
                    )

                    await session.merge(user)
                    await event.answer('Аккаунт успішно зареєстрован!')

        return await handler(event, data)