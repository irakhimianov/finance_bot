from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.inline import statistics_kbd
from loader import dp, bot
from filters import IsAdmin
from database import requests


@dp.callback_query_handler(IsAdmin(), text='statistics')
async def cmd_statistics(call: types.CallbackQuery):
    text = 'Выбери статистику'
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=statistics_kbd
    )
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(IsAdmin(), text_contains='statistics_')
async def get_statistics_interval(call: types.CallbackQuery, session: AsyncSession):
    call_data = call.data.split('_')[-1]
    if call_data == 'today':
        text = await requests.get_today_statistics(session=session)
    elif call_data == 'month':
        text = await requests.get_month_statistics(session=session)
    await bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text
    )
    await bot.answer_callback_query(callback_query_id=call.id)
