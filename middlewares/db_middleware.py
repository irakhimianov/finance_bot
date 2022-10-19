from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


class DBMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, db_factory: sessionmaker):
        super().__init__()
        self.db_factory = db_factory

    async def pre_process(self, obj, data, *args):
        session: AsyncSession = self.db_factory()
        data['session'] = session

    async def post_process(self, obj, data, *args):
        session: AsyncSession = data.get('session')
        await session.close()
