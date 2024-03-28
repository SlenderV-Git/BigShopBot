from aiogram.types import CallbackQuery, Message
from typing import Any
from app.dialogs.admin.astates import AdminPanel, Mailing, AdminReq, UserReports, AdminFreeQuestion, QuestionGroup, OrderChange
from aiogram_dialog import DialogManager

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
    await manager.start(OrderChange.order_view, data={"user_id" : item_id})
    