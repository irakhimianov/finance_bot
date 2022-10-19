from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline import main_kbd
from loader import dp, bot
from filters import IsAdmin


@dp.message_handler(IsAdmin(), CommandStart())
async def cmd_start(message: types.Message):
    # Command '/start' handler
    text = f'Привет!\nСегодня <b>{datetime.now().strftime("%d.%m.%Y")}</b>'
    await message.answer(
        text=text,
        reply_markup=main_kbd
    )


@dp.callback_query_handler(IsAdmin(), text='back_to_main', state='*')
async def back_to_main(call: types.CallbackQuery, state: FSMContext):
    if await state.get_state():
        await state.finish()
    text = f'Привет!\nСегодня <b>{datetime.now().strftime("%d.%m.%Y")}</b>'
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=main_kbd
    )
    await bot.answer_callback_query(callback_query_id=call.id)
