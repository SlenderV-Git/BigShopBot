import logging
from typing import Any
from magic_filter import F
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog import Window, Data, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Button, Column, Row
from aiogram_dialog.widgets.text import Format, Const
from . import keyboards, selected
from .states import BotMenu, Consultation, Question, TechSupport, PaidQuestion, FreeQuestion, Cooperation, FAQ, Courses
from enum import Enum
from aiogram_dialog.widgets.kbd import SwitchInlineQuery
from aiogram_dialog.widgets.text import Const
from app.dialogs.main_dialog.lexicon import faq
from app.db.repo import Repo
from typing import Dict


def main_menu():
    return Window(
        Const('Главное меню'),
        Column(
            Button(Const("Мои заказы"), id="orders"),
            Button(Const("Консультация"), id="consul", on_click=selected.to_consultation),
            Button(Const("Задать вопрос"), id="question", on_click=selected.to_question),
            Button(Const("Курс"), id="course", on_click=selected.to_courses),
            Button(Const("Сотрудничество"), id="coop", on_click=selected.to_cooperation),
            Button(Const("FAQ"), id="faq", on_click=selected.to_faq),
            Button(Const("Админ панель"), id="admin", on_click=selected.go_admin, when="is_admin")
        ),
        getter=get_user,
        state=BotMenu.main_menu  
    )

async def get_user(**kwargs):
    manager : DialogManager = kwargs.get("dialog_manager")
    repo : Repo = manager.middleware_data.get("repo")
    admins = await repo.get_admins()
    return {
        "is_admin" : manager.event.from_user.id in admins
    }
    
def w_cosultation():
    return Window(
        Const("Прежде чем записываться на консультацию, ознакомься со следующей информацией: ""хххххххх"""),
        Row(
            Button(Const("Согласен"), id='consul_accept', on_click= selected.consul_accept_process),
            Cancel(Const("Не согласен"), id = "consul_deny")
        ),
        state=Consultation.info
    )

def consul_info():
    return Window(
        Const("Введите имя"),
        state=Consultation.name
    )

def w_question():
    return Window(
        Const("У тебя есть возможность задать свой вопрос автору, но нет гарантии, что получишь на него ответ: может не быть времени, возможности, желания, и так далее. Также у тебя есть возможность задать платный вопрос, на который получишь гарантированный ответ. Стоимость Х рублей."),
        Column(
            Button(Const("Бесплатный вопрос"), id="free_question", on_click=selected.to_free_question),
            Button(Const("Обращение в техподдержку"), id="tech_sup", on_click=selected.to_support),
            Button(Const("Платный вопрос"), id="paid_question", on_click=selected.to_paid_question),
        ),
        state=Question.title_group
    )
def free_question():
    return Window(
        Const("Можешь написать свой вопрос и отправить. Максимум символов: 1000"),
        Cancel(Const("Отмена"), id="question_cancel"),
        TextInput(id='quest_input', on_success=selected.on_free_question),
        state=FreeQuestion.input_text_question
    )
    
def finish_free_question():
    return Window(
        Const("Сообщение отправлено."),
        state=FreeQuestion.finish_input
    )
    

def tech_support():
    return Window(
        Const("Опишите свою проблему. Макс символов 1000"),
        TextInput(id='supp_appeal', on_success=selected.on_finish_tech),
        Cancel(Const("Отмена"), id="tech_cancel"),
        state = TechSupport.input_text_appeal
    )

def finish_tech_support():
    return Window(
        Const("Обращение успешно отправлено"),
        state = TechSupport.finish_input
    )
def paid_question():
    return Window(
        Const("Выберите способ оплаты"),
        Column(
            Button(Const("Ю-касса"), id="uou_kassa", on_click= selected.send_cassa_order),
            Button(Const("Вид оплаты"), id="suc_payment", on_click=selected.on_suc_question_payment),
            Button(Const("Вид оплаты"), id="unsuc_payment", on_click=selected.on_unsuc_question_payment)
        ),
        Cancel(Const("Отмена")),
        state= Question.select_paid_metod
    )
    
def w_suc_payment():
    return Window(
        Const("Успешная оплата"),
        Button(Const("Отправить вопрос"), id="send_pay_question", on_click=selected.on_question_input),
        Cancel(Const("Отмена")),
        state=PaidQuestion.successful_payment
    )
    
def w_question_input():
    return Window(
        Const("Можешь написать свой вопрос и отправить. Максимум символов: 1000"),
        Cancel(Const("Отмена"), id="question_cancel"),
        TextInput(id='pay_quest_input', on_success=selected.on_suc_question_send),
        state=PaidQuestion.input_text_question
    )

def w_suc_pay_send():
    return Window(
        Const("Обращение успешно отправлено"),
        state = PaidQuestion.finish_input
    )
    
def w_unsuc_payment():
    return Window(
        Const("Ошибка оплаты"),
        Cancel(Const("Повторить")),
        state=Question.unsuccessful_payment
    )
    
def w_courses():
    return Window(
        Const("Курсы"),
        Column(
            Button(Const("Название"), id="couse_id")
        ),
        Cancel(Const("В главное меню")),
        state=Courses.show_course_list
    )

def view_course_description():
    return Window(
    )

def w_cooperation():
    return Window(
        Const("По поводу сотрудничества отправьте сообщения на XXXXX"),
        Cancel(Const("В главное меню")),
        state=Cooperation.contacts
    )
    
def w_faq():
    return Window(
        Const("FAQ"),
        Column(
            *[Button(Const(text), id=text, on_click=selected.current_faq) for text in list(faq.keys())]
        ),
        Cancel(Const("В главное меню")),
        state=FAQ.faq_menu
    )
def cur_faq():
    return Window(
        Format("{dialog_data[type_faq]}"),
        Button(Const("Консультации"), id="go_consul", on_click=selected.to_consultation, when=F["dialog_data"]["consul"]),
        Button(Const("Курсы"), id="go_course", on_click=selected.to_courses, when=F["dialog_data"]["course"]),
        Cancel(Const("В главное меню")),
        state=FAQ.cur_faq
    )


    
