# import asyncio
#
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
# from sqlalchemy.orm import sessionmaker
#
# from database import Base, Category, Expense
# from database import requests
#
#
# async def main():
#     engine = create_async_engine(url='sqlite+aiosqlite:///db.db', echo=True)
#     async with engine.begin() as connection:
#         await connection.run_sync(Base.metadata.create_all)
#
#     async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
#     # session = Session()
#     async with async_session() as session:
#         # categories = await requests.get_all_categories(session=session)
#         # print(categories)
#         # for cat in categories:
#         #     cat: Category
#         #     print(cat)
#         #     print(cat.codename, cat.name)
#         x = await requests.get_month_statistics(session)
# if __name__ == '__main__':
#     asyncio.run(main())
import os
from dotenv import load_dotenv

load_dotenv()

test = os.getenv('test')
print(test)