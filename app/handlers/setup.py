from aiogram import Router
from app.dialogs import setup_dial, setup_admin


def get_router():
    from .private import private_router
    from .admin import admin_router

    router = Router()
    
    router.include_router(setup_dial(private_router))
    router.include_router(setup_admin(admin_router))
    
    return router
