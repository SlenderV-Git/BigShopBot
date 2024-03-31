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
            awindows.order_page_admin(),
            awindows.add_private_channel(),
        ),
        Dialog(
            awindows.admin_finish_payment(),
            awindows.admin_add_url(),
            awindows.admin_add_document()
        ),
        Dialog(
            awindows.start_meiling(),
            awindows.finish_mailing()
        ),
        Dialog(
            awindows.user_report(),
        ),
        Dialog(
            awindows.admin_free_answer(),
            awindows.finish_free_answer()
        ),
        Dialog(
            awindows.course_list_admin(),
            awindows.course_page()
        ),
        Dialog(
            awindows.admin_add_title(),
            awindows.admin_add_description(),
            awindows.admin_add_cost(),
            awindows.admin_add_bonus(),
            awindows.finish_add_couse()
        )
    ]
