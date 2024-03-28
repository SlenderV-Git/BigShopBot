from aiogram import Dispatcher, Router
from . import main_dialog
from . import admin
from . import consultation

def setup_dial(rt : Router):
    rt.include_routers(*main_dialog.bot_menu_dialogs())
    rt.include_routers(*consultation.consul_menu_dialog())
    return rt

def setup_admin(rt : Router):
    rt.include_routers(*admin.admin_menu_dialog())
    return rt