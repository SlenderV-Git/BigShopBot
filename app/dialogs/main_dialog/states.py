from aiogram.filters.state import State, StatesGroup


class BotMenu(StatesGroup):
    main_menu = State()
    
class Question(StatesGroup):
    title_group = State()
    select_paid_metod = State()
    unsuccessful_payment = State()

class FreeQuestion(StatesGroup):
    input_text_question = State()
    finish_input = State()
    
class TechSupport(StatesGroup):
    input_text_appeal = State()
    finish_input = State()

class PaidQuestion(StatesGroup):
    successful_payment = State()
    input_text_question = State()
    finish_input = State()

class Courses(StatesGroup):
    show_course_list = State()
    course_desription = State()
    terms_agreement = State()
    unsuc_payment = State()
    
class GoneCourses(StatesGroup):
    suc_payment = State()

class Cooperation(StatesGroup):
    contacts = State()

class FAQ(StatesGroup):
    faq_menu = State()
    cur_faq = State()
    
class OrdersList(StatesGroup):
    orders_start = State()

class SendDoneDoc(StatesGroup):
    send_done_doc = State()
    finish_doc = State()