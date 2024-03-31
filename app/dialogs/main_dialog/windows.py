import logging
import operator
from typing import Any
from magic_filter import F
from aiogram import Bot
from aiogram.enums import ContentType
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog import Window, Data, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Button, Column, Row, ListGroup, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Format, Const, Jinja
from . import keyboards, selected
from .states import BotMenu, Question, TechSupport, PaidQuestion, FreeQuestion, Cooperation, FAQ, Courses, OrdersList, SendDoneDoc, GoneCourses
from enum import Enum
from aiogram_dialog.widgets.kbd import SwitchInlineQuery
from aiogram_dialog.widgets.text import Const
from app.dialogs.main_dialog.lexicon import faq
from app.db.repo import Repo
from typing import Dict
from app.dialogs.consultation.consul_selected import to_consultation
from datetime import date


def main_menu():
    return Window(
        Const('Главное меню'),
        Column(
            Button(Const("Мои заказы"), id="orders", on_click=selected.to_orders_list),
            Button(Const("Консультация"), id="consul", on_click=to_consultation),
            Button(Const("Задать вопрос"), id="question", on_click=selected.to_question),
            Button(Const("Курс"), id="course", on_click=selected.to_courses),
            Button(Const("Сотрудничество"), id="coop", on_click=selected.to_cooperation),
            Button(Const("FAQ"), id="faq", on_click=selected.to_faq),
            Button(Const("Админ панель"), id="admin", on_click=selected.go_admin, when="is_admin")
        ),
        getter=get_user,
        state=BotMenu.main_menu  
    )


async def get_courses(**kwargs):
    manager : DialogManager = kwargs.get("dialog_manager")
    repo : Repo = manager.middleware_data.get("repo")
    courses_data = await repo.get_courses()
    return {
        'courses' : [(item[1], item[0]) for item in courses_data],
        'is_added' : False if courses_data else True
    }

async def get_user(**kwargs):
    manager : DialogManager = kwargs.get("dialog_manager")
    repo : Repo = manager.middleware_data.get("repo")
    admins = await repo.get_admins()
    return {
        "is_admin" : manager.event.from_user.id in admins
    }
    
def w_question():
    return Window(
        Const("У тебя есть возможность задать свой вопрос автору, но нет гарантии, что получишь на него ответ: может не быть времени, возможности, желания, и так далее. Также у тебя есть возможность задать платный вопрос, на который получишь гарантированный ответ. Стоимость Х рублей."),
        Column(
            Button(Const("Бесплатный вопрос"), id="free_question", on_click=selected.to_free_question),
            Button(Const("Обращение в техподдержку"), id="tech_sup", on_click=selected.to_support),
            Button(Const("Платный вопрос"), id="paid_question", on_click=selected.to_paid_question),
        ),
        Cancel(Const("Отмена")),
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
        Cancel(Const("Отмена")),
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
        Cancel(Const("Отмена")),
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
        Cancel(Const("Отмена")),
        state = PaidQuestion.finish_input
    )
    
def w_unsuc_payment():
    return Window(
        Const("Ошибка оплаты"),
        Cancel(Const("Повторить")),
        Cancel(Const("Отмена")),
        state=Question.unsuccessful_payment
    )
    
def w_courses():
    return Window(
        Const("Курсы"),
        Const("Нет доступных курсов", when= "is_added"),
        ScrollingGroup(
            Select(
                Format('{item[0]}'),
                id="cource_item",
                item_id_getter=operator.itemgetter(1),
                items="courses",
                on_click=selected.cur_course
            ),
            id="couce_list",
            height=6,
            width=1
        ),
        Cancel(Const("В главное меню")),
        getter=get_courses,
        state=Courses.show_course_list
    )

def view_course_description():
    return Window(
        Format("{dialog_data[cur]}"),
        Button(Const("Купить"), id = "buy_course", on_click=selected.buy_courses_page),
        Cancel(Const("Отмена")),
        state=Courses.course_desription
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
        Button(Const("Консультации"), id="go_consul", on_click=to_consultation, when=F["dialog_data"]["consul"]),
        Button(Const("Курсы"), id="go_course", on_click=selected.to_courses, when=F["dialog_data"]["course"]),
        Cancel(Const("В главное меню")),
        state=FAQ.cur_faq
    )

def order_page():
    return Window(
        Const("Список заказов\n"),
        Jinja("""{{title}}
{% for text_item, data_item in consul %}
        * {{ text_item |capitalize }} - {{ data_item }}
{% endfor %}
                """
            ),
        Format("Ваши купленные курсы:\n{courses}", when="course_added"),
        Format("Ваша ссылка на приватную группу: {private_url}", when="approved"),
        Format("Ссылка на оплату: {pay_url}", when="payment"),
        Button(Const("Отравить подписанный документ"), id = "send_done_document", on_click=selected.to_send_doc, when="payment"),
        Cancel(Const("В главное меню")),
        getter= get_orders,
        state= OrdersList.orders_start
    )

def send_doc_page():
    return Window(
        Const("Отправьте подписанный документ"),
        MessageInput(func=selected.finish_done_doc, content_types=ContentType.DOCUMENT),
        Cancel(Const("Отмена")),
        state=SendDoneDoc.send_done_doc
    )
def finish_doc_page():
    return Window(
        Const("Документ отправлен на рассмотрение, следите за статусом заявки в Мои заявки"),
        Cancel(Const("Отмена")),
        state=SendDoneDoc.finish_doc
    )
    
async def get_orders(**kwargs):
    manager : DialogManager = kwargs.get("dialog_manager")
    bot : Bot = kwargs.get("bot")
    repo : Repo = manager.middleware_data.get("repo")
    order_data = await repo.get_order_data(manager.event.from_user.id)
    status = await repo.get_status(manager.event.from_user.id)
    
    text = ("Дата создания заявки", "Дата изменения статуса заявки", "Статус обработки заявки", "Ваши ответы")
    
    if not order_data:
        consul_data = [("", "Нет записей на консультацию")]
        url = "",
        pay_url = ""
    else:
        result = []
        for order in order_data:
            if isinstance(order, date):
                result.append(order.strftime("%Y-%m-%d"))
            else:
                result.append(order)
        order_data = result
        url = await repo.get_access(manager.event.from_user.id)
        doc_id, pay_url = await repo.get_payment_data(manager.event.from_user.id)
        consul_data = [(text_item , data_item) for text_item, data_item in zip(text, order_data)]
        if doc_id:
            await bot.send_document(chat_id= manager.event.message.chat.id, document=doc_id)
    
    courses = await repo.get_sell_courses(manager.event.from_user.id)
    if courses:
        course_sells = "\n\n".join(["\n".join(course) for course in courses])
        
    
    return {
        "consul" : consul_data,
        "title" : "Записи на консультацию:",
        "private_url" : url,
        "pay_url" : pay_url,
        "approved" : status == "access",
        "payment" : status == "payment",
        "courses" : course_sells if courses else "",
        "course_added" : True if courses else False
    }


def finish_course():
    return Window(
        Format("{start_data[course]}"),
        Cancel(Const("Назад")),
        state= GoneCourses.suc_payment
    )