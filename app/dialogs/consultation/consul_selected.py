from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

from app.dialogs.consultation.consul_states import Consultation
from app.dialogs.main_dialog.lexicon import faq
from app.services.payment import send_order
from app.db.repo import Repo
from app.dialogs.consultation.consul_config import quiz
from datetime import datetime

async def to_consultation(c: CallbackQuery, widget: Any, manager: DialogManager):
    repo : Repo = manager.middleware_data.get("repo")
    quiz_data = await repo.get_quiz_data(manager.event.from_user.id)
    if  not quiz_data:
        await repo.add_quiz_data(0, manager.event.from_user.id, " ")
        quiz_data = await repo.get_quiz_data(manager.event.from_user.id)
    cur_quiz, answer_data = quiz_data
    await manager.start(Consultation.info, data={"quiz" : quiz, "cur_quiz" : cur_quiz, "answer_data" : answer_data.split("\n")})

async def consul_accept_process(c: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(manager.start_data)
    repo : Repo = manager.middleware_data.get("repo")
    cur_quiz, answer_data = await repo.get_quiz_data(manager.event.from_user.id)
    if cur_quiz == len(quiz):
        await manager.switch_to(Consultation.finish_quiz)
    else:
        await manager.switch_to(Consultation.quiz_step)
    
async def process_answer(message : Message, widget: Any, manager: DialogManager, data):
    cur_quiz = manager.dialog_data["cur_quiz"]
    quiz = manager.dialog_data["quiz"]
    answer_data : list = manager.dialog_data["answer_data"]
    answer_data.append(f"{quiz[cur_quiz]}\t Ответ: {data}")
    repo : Repo = manager.middleware_data.get("repo")
    user_id = manager.event.from_user.id
    await repo.set_field_data(cur_quiz=cur_quiz + 1, user_tg_id=user_id, field="\n".join(answer_data))
    
    manager.dialog_data["answer_data"] = answer_data
    
    if cur_quiz + 1 < len(quiz):
        manager.dialog_data["cur_quiz"] = cur_quiz + 1
    else:
        await manager.switch_to(Consultation.finish_quiz)
    print(data)
    
async def create_order(c: CallbackQuery, widget: Any, manager: DialogManager):
    repo : Repo = manager.middleware_data.get("repo")
    answer_data : list = manager.dialog_data["answer_data"]
    if not await repo.get_order_data(manager.event.from_user.id):
        await repo.create_order_data(field="\n".join(answer_data), user_tg_id=manager.event.from_user.id)
    await manager.switch_to(Consultation.send_order)