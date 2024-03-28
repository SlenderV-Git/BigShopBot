from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

from app.dialogs.main_dialog.states import BotMenu, Question, TechSupport, PaidQuestion, FreeQuestion, Cooperation, FAQ, Courses, OrdersList, SendDoneDoc
from app.dialogs.main_dialog.lexicon import faq
from app.services.payment import send_order
from app.db.repo import Repo
from app.dialogs.admin.astates import AdminPanel

async def to_question(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(Question.title_group)
    
async def on_finish_tech(message : Message, widget: Any, manager: DialogManager, data):
    print(data)
    repo: Repo = manager.middleware_data.get('repo')
    await repo.create_appeal(field=data, user_tg_id=message.from_user.id)
    await manager.start(TechSupport.finish_input)    
    
    
async def to_support(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(TechSupport.input_text_appeal)
    
    

async def to_paid_question(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(Question.select_paid_metod)
    
async def on_suc_question_payment(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(PaidQuestion.successful_payment)

async def on_unsuc_question_payment(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(Question.unsuccessful_payment)

async def on_question_input(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(PaidQuestion.input_text_question)
    
async def on_suc_question_send(message: Message, widget: Any, manager: DialogManager, data):
    print(data)
    repo: Repo = manager.middleware_data.get('repo')
    await repo.create_paid_question(field=data, user_tg_id=message.from_user.id)
    await manager.switch_to(PaidQuestion.finish_input)
    
    
async def to_cooperation(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(Cooperation.contacts)

async def to_free_question(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(FreeQuestion.input_text_question)

async def on_free_question(message : Message, widget: Any, manager: DialogManager, data):  # Обращение
    repo: Repo = manager.middleware_data.get('repo')
    await repo.create_free_question(field=data, user_tg_id=message.from_user.id)
    await manager.switch_to(FreeQuestion.finish_input) 
    

async def to_courses(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(Courses.show_course_list)

async def to_faq(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(FAQ.faq_menu)
    
async def current_faq(c: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data["type_faq"] = faq[c.data]
    manager.dialog_data["course"] = c.data == "course"
    manager.dialog_data["consul"] = c.data == "consul"
    await manager.switch_to(FAQ.cur_faq)
    
async def send_cassa_order(callback : CallbackQuery, widget: Any, manager: DialogManager):
    await callback.answer()
    await send_order(message = callback.message, bot=callback.message.bot, order_name="add_money")

async def go_admin(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(AdminPanel.admin_menu)
    
async def to_orders_list(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(OrdersList.orders_start)

async def to_send_doc(c: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(SendDoneDoc.send_done_doc)

async def finish_done_doc(message : Message, widget: Any, manager: DialogManager):
    repo : Repo = manager.middleware_data.get("repo")
    await repo.set_done_doc(manager.event.from_user.id, message.document.file_id)
    await manager.switch_to(SendDoneDoc.finish_doc)
