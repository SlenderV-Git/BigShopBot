from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, ContentType, PreCheckoutQuery
from fluentogram import TranslatorRunner, TranslatorHub
from aiogram_dialog import DialogManager, StartMode

from app.db.repo import Repo
from app.utils.callback_data import LangCallbackData
from app.utils.generators import get_start_inline_keyboard, get_lang_select_keyboard
from app.dialogs.main_dialog.states import BotMenu, PaidQuestion
from app.services.payment import send_order
from app.db.models import User
from app.filters.admin_filter import IsAdmin

private_router = Router()
private_router.message.filter(F.chat.type == "private")
private_router.callback_query.filter(F.message.chat.type == "private")


@private_router.message(Command(commands="start"))
async def cmd_start(message: Message, dialog_manager : DialogManager):
    await dialog_manager.start(BotMenu.main_menu, mode=StartMode.RESET_STACK)


@private_router.pre_checkout_query()
async def pre_checkout_process(checkout : PreCheckoutQuery):
    await checkout.bot.answer_pre_checkout_query(checkout.id, ok=True)
    
@private_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def suc_paument(message : Message, dialog_manager : DialogManager):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await dialog_manager.start(PaidQuestion.successful_payment)


    





















'''@private_router.callback_query(F.data == "change_lang")
async def cb_change_lang(query: CallbackQuery, i18n: TranslatorRunner):
    await query.answer()
    text = i18n.change.lang.menu()
    await query.message.edit_text(text=text, reply_markup=get_lang_select_keyboard())


@private_router.callback_query(LangCallbackData.filter())
async def cb_change_lang(
    query: CallbackQuery,
    i18n_hub: TranslatorHub,
    callback_data: LangCallbackData,
    repo: Repo,
):
    i18n = i18n_hub.get_translator_by_locale(callback_data.lang_code)
    await query.answer(i18n.change.lang.success())
    await repo.change_user_lang(query.from_user.id, callback_data.lang_code)
    await query.message.delete()
    await cmd_start(query.message, i18n, query.from_user)'''
