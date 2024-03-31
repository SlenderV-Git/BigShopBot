from aiogram.types import CallbackQuery, Message
from typing import Any
from app.dialogs.admin.astates import (AdminPanel, 
                                       Mailing, 
                                       AdminReq, 
                                       UserReports, 
                                       AdminFreeQuestion, 
                                       QuestionGroup, 
                                       OrderChange, 
                                       PaymentData, 
                                       CourseList,
                                       AddingCourse)
from aiogram_dialog import DialogManager
from app.db.repo import Repo
from time import sleep

async def to_requests(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(AdminReq.admin_req)
    
async def to_user_report(c : CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(UserReports.user_report)

async def to_mailing(c : CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(Mailing.mailing_start)
    
    
async def on_free_selected(callback: CallbackQuery, widget: Any,
                            manager: DialogManager, item_id: str):
    await manager.start(AdminFreeQuestion.input_answer, data={"user_id" : item_id})
    
async def send_answer(message : Message, widget: Any, manager: DialogManager, data):
    user_id = manager.start_data.get("user_id")
    await message.bot.send_message(chat_id= int(user_id), text= str(data))
    await manager.switch_to(AdminFreeQuestion.finish_answer)

async def to_free_quest(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(QuestionGroup.free_questin)
    
async def to_paid_quest(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(QuestionGroup.paid_question)
    
async def to_tech_supp(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(QuestionGroup.tech_supp)
    
async def to_consul_list(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(QuestionGroup.consul_list)
    
    
async def on_consul_selected(callback: CallbackQuery, widget: Any,
                            manager: DialogManager, item_id: str):
    repo : Repo = manager.middleware_data.get("repo")
    done_doc = await repo.get_done_doc(int(item_id))
    if done_doc:
        await callback.bot.send_document(chat_id=callback.message.chat.id, document=done_doc)
    await manager.start(OrderChange.order_view, data={"user_id" : item_id})

async def add_channel_id(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(OrderChange.input_channel)
    
    
async def add_channel_operator(message : Message, widget: Any, manager: DialogManager, data):
    repo : Repo = manager.middleware_data.get("repo")
    user_id = manager.start_data["user_id"]
    await repo.add_channel(user_id=int(user_id), channel_id=data)
    await manager.start(AdminFreeQuestion.finish_answer)
    
async def go_payment(c: CallbackQuery, widget: Any, manager: DialogManager):
    user_id = manager.start_data["user_id"]
    await manager.start(PaymentData.input_document, data={"user_id" : int(user_id)})

async def on_input_doc(message : Message, widget: Any, manager: DialogManager):
    manager.dialog_data["doc_id"] = message.document.file_id
    await manager.switch_to(PaymentData.input_url)

async def on_input_url(message : Message, widget: Any, manager: DialogManager, data):
    repo : Repo = manager.middleware_data.get("repo")
    doc_id = manager.dialog_data["doc_id"]
    user_id = manager.start_data["user_id"]
    await repo.add_payment_data(user_id=user_id, url_pay=data, doc_id=doc_id)
#    await message.bot.send_document(chat_id=message.chat.id, document= doc_id)
    await manager.switch_to(PaymentData.finish_input)
    
async def send_maili(message : Message, widget: Any, manager: DialogManager, data):
    print(data)
    await manager.switch_to(Mailing.finish_mailing)
    repo : Repo = manager.middleware_data.get("repo")
    users : list = await repo.active_users()
    for user in users:
        try:
            await message.forward(chat_id=user)
        except:
            print("NotFound")
        sleep(1)
        
async def to_courses_list(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(CourseList.course_list)
    
async def on_cur_course(callback: CallbackQuery, widget: Any,
                            manager: DialogManager, item_id: str):
    manager.dialog_data["item"] = int(item_id)
    await manager.switch_to(CourseList.cur_course)

async def start_add(callback: CallbackQuery, widget: Any,
                            manager: DialogManager):
    await manager.start(AddingCourse.add_title)

async def add_title(message : Message, widget: Any, manager: DialogManager, data):
    manager.dialog_data["title"] = data
    await manager.switch_to(AddingCourse.add_description)
    
async def on_add_description(message : Message, widget: Any, manager: DialogManager, data):
    manager.dialog_data["description"] = data
    await manager.switch_to(AddingCourse.add_cost)
    
async def on_add_cost(message : Message, widget: Any, manager: DialogManager, data : str):
    if data.isdigit():
        manager.dialog_data["cost"] = int(data)
        await manager.switch_to(AddingCourse.add_bonus)

async def on_add_bonus(message : Message, widget: Any, manager: DialogManager, data):
    title = manager.dialog_data.get("title")
    description = manager.dialog_data.get("description")
    cost = manager.dialog_data.get("cost")
    repo : Repo = manager.middleware_data.get("repo")
    await repo.add_course(title=title, description=description, cost=cost, after_buy_content=data)
    await manager.switch_to(AddingCourse.finish_add)