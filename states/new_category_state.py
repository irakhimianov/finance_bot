from aiogram.dispatcher.filters.state import State, StatesGroup


class AddNewCategory(StatesGroup):
    codename = State()
    name = State()
    aliases = State()
