from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class Admin(StatesGroup):
    id_text = State()

class Payment(StatesGroup):
    hash_ = State()
    period = State()