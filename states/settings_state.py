from aiogram.dispatcher.filters.state import State, StatesGroup


class AddCity(StatesGroup):
    name = State()
