import handlers
import logging

import asyncio
import aioschedule
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from data import config
from database import Base
from loader import dp, bot
from middlewares import DBMiddleware, UserMiddleware
from utils import on_startup_notify, everyday_broadcast, set_default_commands


async def scheduler():
    aioschedule.every().day.at("10:05").do(everyday_broadcast)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup():
    logging.basicConfig(
        format=u'%(filename)s:%(lineno)-d #%(levelname)-16s [%(asctime)s] %(message)s',
        level=logging.INFO
    )
    # DB
    logging.info('DB connecting...')
    # db_engine = create_async_engine(url='sqlite+aiosqlite:///db.db')
    url = f'postgresql+asyncpg://{config.PG_USER}:{config.PG_PASSWORD}@{config.PG_HOST}:{config.PG_PORT}/{config.PG_DB}'
    db_engine = create_async_engine(url=url)

    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    db_factory = sessionmaker(bind=db_engine, class_=AsyncSession, expire_on_commit=False)
    logging.info('DB connected!')

    # middlewares
    logging.info('Setting up middlewares...')
    dp.setup_middleware(DBMiddleware(db_factory))
    dp.setup_middleware(UserMiddleware())
    logging.info('Middlewares has been set')

    logging.info('Everything is ready to launch!')
    # Set default commands (/start and /help)
    await set_default_commands(dp)

    # Notify admin that the bot has started
    await on_startup_notify()
    asyncio.create_task(scheduler())
    await dp.skip_updates()
    await dp.start_polling()


async def on_shutdown():
    logging.info('Shutting down...')
    await dp.storage.close()
    await dp.storage.wait_closed()
    bot_session = await bot.get_session()
    await bot_session.close()


async def main():
    try:
        await on_startup()
    finally:
        await on_shutdown()


if __name__ == '__main__':
    # Launch bot
    asyncio.get_event_loop().run_until_complete(main())
