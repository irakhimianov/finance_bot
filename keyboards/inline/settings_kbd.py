from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline import back_to_main


settings_kbd = InlineKeyboardMarkup(row_width=2)
buttons = [
    InlineKeyboardButton(text='Установить город', callback_data='settings_city'),
]
settings_kbd.add(*buttons)
settings_kbd.add(back_to_main)
