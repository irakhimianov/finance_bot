from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio.session import AsyncSession

from database import requests
from keyboards.inline import categories_kbd, cancel_kbd
from loader import dp, bot
from filters import IsAdmin
from states import AddNewCategory


@dp.callback_query_handler(IsAdmin(), text='add_category', state=None)
async def cmd_new_category(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['chat_id'] = call.message.chat.id
        data['last_message_id'] = call.message.message_id
    text = 'Отправь уникальный <b>codename</b>'
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=cancel_kbd
    )
    await AddNewCategory.codename.set()
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.message_handler(IsAdmin(), state=AddNewCategory.codename)
async def cmd_category_codename(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['codename'] = message.text.strip().lower()
        chat_id = data['chat_id']
        last_message_id = data['last_message_id']
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    text = 'Введите уникальное <b>имя (name)</b>'
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=last_message_id,
        text=text,
        reply_markup=cancel_kbd
    )
    await AddNewCategory.name.set()


@dp.message_handler(IsAdmin(), state=AddNewCategory.name)
async def cmd_category_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text.strip().lower()
        chat_id = data['chat_id']
        last_message_id = data['last_message_id']
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    text = 'Введите через пробел <b>альясы (ключевые слова) для поиска</b>'
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=last_message_id,
        text=text,
        reply_markup=cancel_kbd
    )
    await AddNewCategory.aliases.set()


@dp.message_handler(IsAdmin(), state=AddNewCategory.aliases)
async def cmd_category_aliases(message: types.Message, session: AsyncSession, state: FSMContext):
    async with state.proxy() as data:
        data['aliases'] = message.text
        chat_id = data['chat_id']
        last_message_id = data['last_message_id']
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await bot.delete_message(
        chat_id=chat_id,
        message_id=last_message_id
    )
    text = 'Категория успешно добавлена'
    await bot.send_message(
        chat_id=message.chat.id,
        text=text
    )
    data = await state.get_data()
    await requests.db_add_category(
        session=session,
        codename=data['codename'],
        name=data['name'],
        aliases=data['aliases']
    )
    await state.finish()
