from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        await self.process_user(message.from_user, data)

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        await self.process_user(call.from_user, data)

    async def process_user(self, user: types.User, data: dict):
        db_user, is_new_user = await self.get_user(user, data['session'])

    @staticmethod
    async def get_user(user: types.User, session: AsyncSession) -> tuple[User, bool]:
        db_user = await session.get(User, user.id)
        is_new_user = False

        if db_user is None:
            db_user = User(telegram_id=user.id)
            session.add(db_user)
            is_new_user = True
        if is_new_user:
            await session.commit()
            await session.refresh(db_user)
        return db_user, is_new_user
