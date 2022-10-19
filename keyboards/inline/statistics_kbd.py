from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline import back_to_main


statistics_kbd = InlineKeyboardMarkup(row_width=2)
buttons = [
    InlineKeyboardButton(text='За сегодня', callback_data='statistics_today'),
    InlineKeyboardButton(text='За месяц', callback_data='statistics_month')
]
statistics_kbd.add(*buttons)
statistics_kbd.add(back_to_main)
