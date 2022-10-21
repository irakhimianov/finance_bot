from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio.session import AsyncSession

from database import requests
from keyboards.inline import categories_kbd, cancel_kbd, settings_kbd, back_to_main_kbd
from loader import dp, bot
from filters import IsAdmin
from states import AddCity


@dp.message_handler(state=AddCity.name)
async def set_user_city(message: types.Message, session: AsyncSession, state: FSMContext):
    async with state.proxy() as data:
        city = message.text
        chat_id = data['chat_id']
        last_message_id = data['last_message_id']
    await requests.set_user_city(
        session=session,
        telegram_id=message.from_user.id,
        city=city
    )
    text = f'Город <b>{city}</b> успешно установлен'
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=last_message_id,
        text=text,
        reply_markup=back_to_main_kbd
    )
    await state.finish()
