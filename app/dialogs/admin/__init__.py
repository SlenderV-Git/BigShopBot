from aiogram_dialog import Dialog

from . import awindows

def admin_menu_dialog():
    return [
        Dialog(
            awindows.main_menu(),  
        ),
        Dialog(
            awindows.list_question(),
        ),
        Dialog(
            awindows.free_quest_list(),
            awindows.paid_quest_list(),
            awindows.tech_supp_list(),
            awindows.aconsul_list(),
            
        ),
        Dialog(
            awindows.order_page_admin()
        ),
        Dialog(
            awindows.start_meiling(),
        ),
        Dialog(
            awindows.user_report(),
        ),
        Dialog(
            awindows.admin_free_answer(),
            awindows.finish_free_answer()
        )
    ]
