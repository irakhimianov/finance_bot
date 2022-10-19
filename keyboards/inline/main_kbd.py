from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main_kbd = InlineKeyboardMarkup(row_width=1)
buttons = [
    InlineKeyboardButton(text='Добавить затраты', callback_data='add_expense'),
    InlineKeyboardButton(text='Добавить категорию', callback_data='add_category'),
    InlineKeyboardButton(text='Статистика', callback_data='statistics'),
    InlineKeyboardButton(text='Настройки', callback_data='settings')
]
main_kbd.add(*buttons)
