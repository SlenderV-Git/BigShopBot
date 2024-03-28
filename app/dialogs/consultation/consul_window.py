from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Cancel, Back, Button, Column, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format, Const, Jinja
from aiogram_dialog.widgets.media import DynamicMedia
from app.dialogs.consultation import consul_selected
from app.dialogs.consultation.consul_states import Consultation
from aiogram_dialog.widgets.input import TextInput, MessageInput
from app.db.repo import Repo
import operator
from datetime import datetime



def w_cosultation():
    return Window(
        Const("Прежде чем записываться на консультацию, ознакомься со следующей информацией: ""хххххххх"""),
        Row(
            Button(Const("Согласен"), id='consul_accept', on_click= consul_selected.consul_accept_process),
            Cancel(Const("Не согласен"), id = "consul_deny")
        ),
        state=Consultation.info
    )

def consul_quiz():
    return Window(
        Format("{cur_quiz}"),
        TextInput(id='pay_quest_input', on_success=consul_selected.process_answer),
        Cancel(Const("Отмена")),
        getter= get_question,
        state=Consultation.quiz_step
    )

async def get_question(**kwargs):
    manager : DialogManager = kwargs.get("dialog_manager")
    quiz_data = manager.dialog_data
    quiz = quiz_data["quiz"]
    cur_quiz = quiz_data["cur_quiz"]
    return {
        "cur_quiz" : quiz[cur_quiz]
    }
    
def finish_quiz_window():
    return Window(
        Format("{answers}"),
        Button(Const("Отправить ответы"), id= "send_quiz", on_click=consul_selected.create_order),
        Cancel(Const("Отмена")),
        state=Consultation.finish_quiz,
        getter=get_answers
    )

async def get_answers(**kwargs):
    manager : DialogManager = kwargs.get("dialog_manager")
    answer_data : list = manager.dialog_data["answer_data"]
    return {
        "answers" : "\n".join(answer_data)
    }

def send_order():
    return Window(
        Const("Заказ успешно создан. В скором времени вы получите данные для оплаты\n Статус заявки смотрите в Мои заказы"),
        Cancel(Const("В главное меню")),
        state=Consultation.send_order
    )
