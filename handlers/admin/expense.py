from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio.session import AsyncSession

from keyboards.inline import categories_kbd, cancel_kbd
from loader import dp, bot
from filters import IsAdmin
from states import AddExpense
from utils import add_expense


@dp.message_handler(IsAdmin())
async def msg_expense(message: types.Message, session: AsyncSession):
    text = await add_expense(message_text=message.text, session=session)
    await message.answer(
        text=text
    )


@dp.callback_query_handler(IsAdmin(), text='add_expense', state=None)
async def cmd_expense(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    kbd = await categories_kbd(session)
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Выбери соответствующую категорию',
        reply_markup=kbd
    )
    async with state.proxy() as data:
        data['chat_id'] = call.message.chat.id
        data['last_message_id'] = call.message.message_id
    await AddExpense.category.set()
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(IsAdmin(), text_contains='category_', state=AddExpense.category)
async def cmd_expense_category(call: types.CallbackQuery, state: FSMContext):
    category_codename = call.data.split('_')[-1]
    async with state.proxy() as data:
        data['category_codename'] = category_codename
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Напиши потраченную сумму',
        reply_markup=cancel_kbd,
    )
    await AddExpense.expense_amount.set()
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.message_handler(IsAdmin(), state=AddExpense.expense_amount)
async def cmd_expense_amount(message: types.Message, session: AsyncSession, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
        category_codename = data['category_codename']
        chat_id = data['chat_id']
        last_message_id = data['last_message_id']
    text = await add_expense(
        message_text=message.text,
        session=session,
        category_codename=category_codename
    )
    await bot.delete_message(
        chat_id=chat_id,
        message_id=last_message_id
    )
    await message.answer(text=text)
    await state.finish()
