from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from app.filters.admin_filter import IsAdmin
from app.dialogs.admin.astates import AdminPanel
from aiogram_dialog import DialogManager, StartMode
from fluentogram import TranslatorRunner, TranslatorHub

from app.db.repo import Repo


admin_router = Router()
admin_router.message.filter(F.chat.type == "private", IsAdmin())
admin_router.callback_query.filter(F.message.chat.type == "private", IsAdmin())

@admin_router.message(Command("admin"))
async def call_admin(message : Message, dialog_manager : DialogManager, i18n : TranslatorRunner):
    await message.answer(i18n.welcome(user = message.from_user.full_name))
    await dialog_manager.start(AdminPanel.admin_menu, mode=StartMode.RESET_STACK)
