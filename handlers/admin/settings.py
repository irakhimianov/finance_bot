from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio.session import AsyncSession

from database import requests
from keyboards.inline import categories_kbd, cancel_kbd, settings_kbd, back_to_main_kbd
from loader import dp, bot
from filters import IsAdmin
from states import AddCity


@dp.callback_query_handler(IsAdmin(), text='settings')
async def cmd_settings(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['chat_id'] = call.message.chat.id
        data['last_message_id'] = call.message.message_id
    text = 'Окно настроек'
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=settings_kbd
    )
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(IsAdmin(), text_contains='settings_')
async def set_user_settings(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data.split('_')[-1]
    text = ''
    async with state.proxy() as data:
        chat_id = data['chat_id']
        last_message_id = data['last_message_id']
    if call_data == 'city':
        await AddCity.name.set()
        text = 'Отправь наименование города, для получения прогноза погоды'
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=last_message_id,
        text=text,
        reply_markup=cancel_kbd
    )
    await bot.answer_callback_query(callback_query_id=call.id)


