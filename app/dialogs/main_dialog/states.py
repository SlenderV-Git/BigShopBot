from aiogram.filters.state import State, StatesGroup


class BotMenu(StatesGroup):
    main_menu = State()
    
class Consultation(StatesGroup):
    info = State()
    name = State()
    birth_date = State()
    phone_number = State()
    meeting_subject = State()
    
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
    course_fees = State()
    suc_payment = State()
    unsuc_payment = State()

class Cooperation(StatesGroup):
    contacts = State()

class FAQ(StatesGroup):
    faq_menu = State()
    cur_faq = State()