from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio.session import AsyncSession

from database import Category, requests
from keyboards.inline import back_to_main


async def categories_kbd(session: AsyncSession) -> InlineKeyboardMarkup:
    kbd = InlineKeyboardMarkup(row_width=2)
    buttons = []
    categories = await requests.get_all_categories(session=session)
    for category in categories:
        category: Category
        buttons.append(
            InlineKeyboardButton(
                text=f'{category.name.capitalize()}',
                callback_data=f'category_{category.codename}')
        )
    kbd.add(*buttons)
    kbd.add(back_to_main)
    return kbd
