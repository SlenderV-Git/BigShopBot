from aiogram import Dispatcher, Router
from . import main_dialog
from . import admin

def setup_dial(rt : Router):
    rt.include_routers(*main_dialog.bot_menu_dialogs())
    # register a dialog
    return rt

def setup_admin(rt : Router):
    rt.include_routers(*admin.admin_menu_dialog())
    return rt