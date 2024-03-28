from aiogram.filters.state import State, StatesGroup

class AdminPanel(StatesGroup):
    admin_menu = State()
    
class UserReports(StatesGroup):
    user_report = State()
    
class Mailing(StatesGroup):
    mailing_start = State()

class AdminReq(StatesGroup):
    admin_req = State()

class QuestionGroup(StatesGroup):
    free_questin = State()
    paid_question = State()
    tech_supp = State()
    consul_list = State()

class OrderChange(StatesGroup):
    order_view = State()
    appove = State()
    input_url = State()
    finish_input = State()


class AdminFreeQuestion(StatesGroup):
    input_answer = State()
    finish_answer = State()
    