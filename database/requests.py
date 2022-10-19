import datetime

from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio.session import AsyncSession

from database import Category, Expense


async def db_add_category(session: AsyncSession, codename: str, name: str, aliases: str):
    # TODO проверка на существование категории
    category = Category(
        codename=codename,
        name=name,
        aliases=aliases
    )
    print(category)
    session.add(category)
    await session.commit()


async def get_category(session: AsyncSession, codename_or_alias: str) -> Category:
    category = await session.execute(
        select(Category).
        where(or_(Category.codename.contains(codename_or_alias), Category.aliases.contains(codename_or_alias)))
    )
    category = category.scalars().first()
    if category is None:
        category = await session.get(Category, 'other')
    return category


async def get_all_categories(session: AsyncSession):
    categories = await session.execute(
        select(Category)
    )
    categories = categories.scalars().all()
    return categories


async def db_add_expense(session: AsyncSession, amount: float, codename_or_alias: str = 'прочее') -> str:
    category: Category = await get_category(session=session, codename_or_alias=codename_or_alias)
    expense = Expense(
        amount=amount,
        category_codename=category.codename
    )
    session.add(expense)
    await session.commit()
    return category.name


async def get_today_statistics(session: AsyncSession) -> str:
    result = 0
    text = ''
    today_expenses = await session.execute(
        select(Expense.created_at, Expense.amount, Category.name).join(Category)
        .where(func.date(Expense.created_at) == func.current_date() and Category.codename == Expense.category_codename)
    )
    today_expenses = today_expenses.all()
    for expense in today_expenses:
        if expense is not None:
            result += expense.amount
            text += f'<u>{expense[0].strftime("%d.%m %H:%M")}</u> - <b>{expense[1]}₽</b> - {expense[2]}\n\n'
    return f'{text}<b>Итого: {result:.2f}₽</b>' if result else 'Никаких затрат сегодня не было'


async def get_month_statistics(session: AsyncSession) -> str:
    now = datetime.datetime.now()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    total_amount = await session.execute(
        select(func.sum(Expense.amount))
        .where(func.date(Expense.created_at) >= func.date(first_day_of_month))
    )
    text = f'За текущий месяц потрачено <b>{total_amount.scalar():.2f}₽</b>\n\n'
    details = await session.execute(
        f'''
            select category.name, sum(expense.amount) as spent,
            (count(expense.category_codename) * 100 / (select count(*) from expense where expense.created_at >= '{first_day_of_month}')) as score
            from category
            join expense on expense.category_codename = category.codename
            where expense.created_at >= '{first_day_of_month}'
            group by category.name
        '''
    )

    for d in details:
        text += f'<u>{d[0].capitalize()}</u> - <b>{d[1]:.2f}₽</b> - {d[2]}%\n'
    return text
