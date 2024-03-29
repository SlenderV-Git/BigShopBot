from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Cancel, Back, Button, Column, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format, Const, Jinja
from app.dialogs.admin import aselected
from app.dialogs.admin.astates import AdminPanel, UserReports, AdminReq, Mailing, AdminFreeQuestion, QuestionGroup, OrderChange, PaymentData
from aiogram_dialog.widgets.input import TextInput, MessageInput
from app.db.repo import Repo
from aiogram.enums import ContentType
import operator
from datetime import datetime, date



def main_menu():
    return Window(
        Const('Админ панель'),
        Column(
            Button(Const("Отчет по пользователям"), id="user_report", on_click=aselected.to_user_report),
            Button(Const("Заявки"), id="requests", on_click=aselected.to_requests),
            Button(Const("Рассылка"), id="mailing", on_click=aselected.to_mailing),
        ),
        Cancel(Const("Назад")),
        state= AdminPanel.admin_menu
    )

def user_report():
    return Window(
        Jinja(
                """
                {{title}}
                Отчет о действиях пользователей на платформе:
                {% for key, value in user_data.items() %}
                 * {{ key |capitalize }} - {{ value }}
                {% endfor %}
                """
            ),
        Cancel(Const("Назад")),
        parse_mode="HTML",
        getter=get_user_report,
        state=UserReports.user_report
    )

async def get_user_report(**kwargs):
    manager : DialogManager = kwargs.get("dialog_manager")
    repo : Repo = manager.middleware_data.get("repo")
    
    user_data = {
        "Всего пользователей бота" : len(await repo.get_users()),
        "Активных пользователей" : len(await repo.active_users()),
        "Администраторов" : len(await repo.get_admins()),
        "Создано бесплатных вопросов" : len(await repo.get_free_quest_data()),
        "Создано платных вопросов" : len(await repo.get_paid_quest_data()),
        "Обращений в тех поддержку" : len(await repo.get_appeal_data()),
        "Зарегистрировано за сегодня" : len(await repo.user_reg_day()),
        "Зарегистрировано за посленюю неделю" : len(await repo.user_reg_week()),
        "Зарегистрировано за последний месяц" : len(await repo.user_reg_month()),
    }
    return {
        "user_data" : user_data
    }
    
    
def list_question():
    return Window(
        Const("Выберите тип заявки"),
        Button(Const("Бесплатные вопросы"), id="on_free_quest", on_click=aselected.to_free_quest),
        Button(Const("Платные вопросы"), id="on_paid_quest", on_click=aselected.to_paid_quest),
        Button(Const("Обращения в тех поддержку"), id="on_tech_supp", on_click=aselected.to_tech_supp),
        Button(Const("Заявки на консультацию"), id = "on_consul_list", on_click=aselected.to_consul_list),
        Cancel(Const("Отмена")),
        state=AdminReq.admin_req

    )

def free_quest_list():
    return Window(
        Format("Актуальный список бесплатных вопросов от пользователей. Дата выставления отчета: {date}"),
        ScrollingGroup(
            Select(
                Format("{item[0]} ({pos}/{data[count]})"),
                id="free_quest",
                item_id_getter=operator.itemgetter(1),
                items="free_items",
                on_click=aselected.on_free_selected
            ),
            id="free_list",
            width=1, 
            height=6
        ),
        Cancel(Const("Назад")),
        getter= get_free_list,
        state= QuestionGroup.free_questin
    )

async def get_free_list(**kwargs):
    manager : DialogManager = kwargs.get("dialog_manager")
    repo : Repo = manager.middleware_data.get("repo")
    req = await repo.get_free_req()
    return {
        "free_items" : req,
        "count": len(req),
        "date" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def paid_quest_list():
    return Window(
        Format("Актуальный список платных вопросов от пользователей. Дата выставления отчета: {date}"),
        ScrollingGroup(
            Select(
                Format("{item[0]} ({pos}/{data[count]})"),
                id="paid_quest",
                item_id_getter=operator.itemgetter(1),
                items="paid_items",
                on_click=aselected.on_free_selected
            ),
            id="paid_list",
            width=1, 
            height=6
        ),
        Cancel(Const("Назад")),
        getter= get_paid_list,
        state= QuestionGroup.paid_question
    )

async def get_paid_list(**kwargs):
    manager : DialogManager = kwargs.get("dialog_manager")
    repo : Repo = manager.middleware_data.get("repo")
    req = await repo.get_paid_req()
    return {
        "paid_items" : req,
        "count": len(req),
        "date" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
def tech_supp_list():
    return Window(
        Format("Актуальный список обращений в техподдержку пользователей. Дата выставления отчета: {date}"),
        ScrollingGroup(
            Select(
                Format("{item[0]} ({pos}/{data[count]})"),
                id="tech_supp",
                item_id_getter=operator.itemgetter(1),
                items="tech_items",
                on_click=aselected.on_free_selected
            ),
            id="tech_list",
            width=1, 
            height=6
        ),
        Cancel(Const("Назад")),
        getter= get_tech_list,
        state= QuestionGroup.tech_supp
    )

async def get_tech_list(**kwargs):
    manager : DialogManager = kwargs.get("dialog_manager")
    repo : Repo = manager.middleware_data.get("repo")
    req = await repo.tech_supp_req()
    return {
        "tech_items" : req,
        "count": len(req),
        "date" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def admin_free_answer():
    return Window(
        Const("Напишите сообщение которое будет отправлено пользователю"),
        Cancel(Const("Отмена"), id="question_cancel"),
        TextInput(id='admin_answer_free', on_success=aselected.send_answer),
        state=AdminFreeQuestion.input_answer
    )

def finish_free_answer():
    return Window(
        Const("Сообщение отправлено."),
        Cancel(Const("Назад")),
        state=AdminFreeQuestion.finish_answer
    )

def aconsul_list():
    return Window(
        Format("Актуальный список заявок на консультацию. Дата выставления отчета: {date}"),
        ScrollingGroup(
            Select(
                Format("{item[0]} Статус заявки: {item[1]} ({pos}/{data[count]})"),
                id="consul_but",
                item_id_getter=operator.itemgetter(2),
                items="consul_items",
                on_click=aselected.on_consul_selected
            ),
            id="consul_list",
            width=1, 
            height=6
        ),
        Cancel(Const("Назад")),
        getter= get_consul,
        state= QuestionGroup.consul_list
    )

async def get_consul(**kwargs):
    manager : DialogManager = kwargs.get("dialog_manager")
    repo : Repo = manager.middleware_data.get("repo")
    req = await repo.get_orders()
    return {
        "consul_items" : req,
        "count": len(req),
        "date" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def order_page_admin():
    return Window(
        Const("Список заказов\n"),
        Jinja("""{{title}}
{% for text_item, data_item in consul %}
        * {{ text_item |capitalize }} - {{ data_item }}
{% endfor %}
                """
            ),
        Button(Const("Подтвердить оплату"), id="aprove", on_click=aselected.add_channel_id),
        Button(Const("Выслать данные для оплаты"), id="send_payment", on_click=aselected.go_payment),
        Cancel(Const("Назад")),
        getter= get_orders_admin,
        state= OrderChange.order_view
    )
    
def admin_add_document():
    return Window(
        Const("Отправьте документ:"),
        Cancel(Const("Отмена")),
        MessageInput(content_types=[ContentType.DOCUMENT], func=aselected.on_input_doc),
        state = PaymentData.input_document
    )

def admin_add_url():
    return Window(
        Const("Отправьте ссылку для оплаты:"),
        Cancel(Const("Отмена")),
        TextInput(id= "payment_url", on_success = aselected.on_input_url),
        state= PaymentData.input_url
    )

def admin_finish_payment():
    return Window(
        Const("Данные для оплаты отправлены пользователю, статус заявки изменен на Ожидает оплаты"),
        Cancel(Const("В главнное меню")),
        state= PaymentData.finish_input
    )
    
def add_private_channel():
    return Window(
        Const("Укажите ссылку на приватный канал"),
        Cancel(Const("Отмена"), id="private_add"),
        TextInput(id='private_add_id', on_success=aselected.add_channel_operator),
        state=OrderChange.input_channel
    )



async def get_orders_admin(**kwargs):
    manager : DialogManager = kwargs.get("dialog_manager")
    repo : Repo = manager.middleware_data.get("repo")
    user_id = manager.start_data["user_id"]
    order_data = await repo.get_order_data(int(user_id))
    if not order_data:
        order_data = "Нет записей на консультацию"
    else:
        result = []
        for order in order_data:
            if isinstance(order, date):
                result.append(order.strftime("%Y-%m-%d"))
            else:
                result.append(order)
        order_data = result
        text = ("Дата создания заявки", "Дата изменения статуса заявки", "Статус обработки заявки", "Ваши ответы")
    return {
        "consul" : [(text_item , data_item) for text_item, data_item in zip(text, order_data)],
        "title" : "Записи на консультацию:"
    }

def start_meiling():
    return Window(
        Const("Рассылка сообщений"),
        Cancel(Const("Назад")),
        state=Mailing.mailing_start
    )