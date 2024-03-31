from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, ContentType, PreCheckoutQuery, ChatMemberUpdated
from fluentogram import TranslatorRunner, TranslatorHub
from aiogram_dialog import DialogManager, StartMode, BaseDialogManager
from aiogram_dialog.manager.bg_manager import BgManagerFactoryImpl
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, MEMBER, KICKED
from app.db.repo import Repo
from app.utils.callback_data import LangCallbackData
from app.utils.generators import get_start_inline_keyboard, get_lang_select_keyboard
from app.dialogs.main_dialog.states import BotMenu, PaidQuestion, GoneCourses
from app.services.payment import send_order
from app.db.models import User
from app.filters.admin_filter import IsAdmin

private_router = Router()
private_router.message.filter(F.chat.type == "private")
private_router.callback_query.filter(F.message.chat.type == "private")


@private_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED)
)
async def user_blocked_bot(event: ChatMemberUpdated, repo : Repo):
    await repo.set_user_active_or_ban(event.from_user.id, False)


@private_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER)
)
async def user_unblocked_bot(event: ChatMemberUpdated, repo : Repo):
    await repo.set_user_active_or_ban(event.from_user.id, True)


@private_router.message(Command(commands="start"))
async def cmd_start(message: Message, dialog_manager : DialogManager):
    await dialog_manager.start(BotMenu.main_menu, mode=StartMode.RESET_STACK)


@private_router.pre_checkout_query(F.invoice_payload.startswith("bying_paid"))
async def pre_checkout_process(checkout : PreCheckoutQuery, dialog_bg_factory : BgManagerFactoryImpl):
    base_dialog : BaseDialogManager = dialog_bg_factory.bg(bot=checkout.bot, 
                                                           user_id=checkout.from_user.id, 
                                                           chat_id=checkout.from_user.id)
    await base_dialog.start(PaidQuestion.successful_paymen)
    await checkout.bot.answer_pre_checkout_query(checkout.id, ok=True)
    
@private_router.pre_checkout_query(F.invoice_payload.startswith("bying_courses"))
async def pre_checkout_process(checkout : PreCheckoutQuery, 
                               dialog_bg_factory : BgManagerFactoryImpl,
                               repo : Repo):
    base_dialog : BaseDialogManager = dialog_bg_factory.bg(bot=checkout.bot, 
                                                           user_id=checkout.from_user.id, 
                                                           chat_id=checkout.from_user.id)
    course_id = int(checkout.invoice_payload.replace("bying_courses_", ""))
    course_data = await repo.get_course_by_id(course_id=course_id)
    await repo.buy_course(course_id=course_id, user_id=checkout.from_user.id)
    await base_dialog.start(GoneCourses.suc_payment, data={
        "course" : course_data[3]
    })
    await checkout.bot.answer_pre_checkout_query(checkout.id, ok=True)
    
@private_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def suc_paument(message : Message, dialog_manager : DialogManager):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
