from aiogram.dispatcher.filters.state import State, StatesGroup


class AddExpense(StatesGroup):
    category = State()
    expense_amount = State()
