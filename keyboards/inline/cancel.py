from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


cancel_button = InlineKeyboardButton(text='Отмена ❌', callback_data='cancel')
cancel_kbd = InlineKeyboardMarkup(row_width=1)
cancel_kbd.add(cancel_button)
