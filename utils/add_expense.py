import logging
import re

from sqlalchemy.ext.asyncio.session import AsyncSession

from database import requests


async def add_expense(message_text: str, session: AsyncSession, category_codename: str = None) -> str:
    full_expense = parse_message(message_text=message_text)

    if isinstance(full_expense, tuple):
        amount, codename_or_alias = full_expense
        category_name = await requests.db_add_expense(
            session=session,
            amount=amount,
            codename_or_alias=codename_or_alias
        )
        text = f'Сумма <b>{amount:.0f} ₽</b> добавлена в категорию <b>{category_name}</b>'

    elif isinstance(full_expense, float) and category_codename:
        category_name = await requests.db_add_expense(
            session=session,
            amount=full_expense,
            codename_or_alias=category_codename
        )
        text = f'Сумма <b>{full_expense:.0f} ₽</b> добавлена в категорию <b>{category_name}</b>'

    elif isinstance(full_expense, float):
        category_name = await requests.db_add_expense(
            session=session,
            amount=full_expense
        )
        text = f'Сумма <b>{full_expense:.0f} ₽</b> добавлена в категорию <b>{category_name}</b>'

    elif isinstance(full_expense, bool) or full_expense is False:
        text = 'Последнее сообщение не распознано.\nПопробуй так: <code>150 такси</code>'
    return text


def parse_message(message_text: str) -> tuple[float, str] | float | bool:
    amount_with_text = re.match(r'^\d+[\.|\,]?\d*( [a-zA-Zа-яА-Я]+)$', message_text)
    just_amount = re.match(r'^\d+[\.|\,]?\d*$', message_text)

    try:
        if amount_with_text and amount_with_text.group(0):
            amount, text = amount_with_text.group(0).split()
            amount = float(amount)
            text = str(text)
            return amount, text

        elif just_amount and just_amount.group(0):
            amount = float(just_amount.group(0))
            return amount

    except Exception as e:
        logging.error(f'Cant parse message: {e}\n{message_text}')
    return False