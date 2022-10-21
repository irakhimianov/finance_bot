from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio.session import AsyncSession

from database import requests
from filters import IsAdmin
from keyboards.inline import categories_kbd, cancel_kbd, settings_kbd, back_to_main_kbd
from loader import dp, bot
from states import AddCity
from utils import get_weather


@dp.message_handler(commands=['weather'])
@dp.message_handler(IsAdmin(), commands=['weather'])
async def cmd_weather(message: types.Message, session: AsyncSession, state: FSMContext):
    user_city = await requests.get_user_city(
        session=session,
        telegram_id=message.from_user.id
    )
    if user_city:
        text = await get_weather(city=user_city)
        await message.answer(text=text)
    else:
        text = f'Город по умолчанию не найден. Отправьте наименование своего города'
        await AddCity.name.set()
        bot_message = await message.answer(text=text, reply_markup=cancel_kbd)
        async with state.proxy() as data:
            data['chat_id'] = message.chat.id
            data['last_message_id'] = bot_message.message_id
