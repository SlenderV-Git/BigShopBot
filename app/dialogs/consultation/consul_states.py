from aiogram.filters.state import State, StatesGroup

class Consultation(StatesGroup):
    info = State()
    quiz_step = State()
    finish_quiz = State()
    send_order = State()
    