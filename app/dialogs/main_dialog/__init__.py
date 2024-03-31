from aiogram_dialog import Dialog

from . import windows


def bot_menu_dialogs():
    return [
        Dialog(
            windows.main_menu(),
        ),
        Dialog(
            windows.w_cooperation(),
        ),
        Dialog(
            windows.w_courses(),
            windows.view_course_description()
        ),
        Dialog(
            windows.w_faq(),
            windows.cur_faq()
        ),
        Dialog(
            windows.w_question(),
            windows.paid_question(),
            windows.w_unsuc_payment(),
        ),
        Dialog(
            windows.free_question(),
            windows.finish_free_question()
        ),
        Dialog(
            windows.tech_support(),
            windows.finish_tech_support()
        ),
        Dialog(
            windows.w_suc_pay_send(),
            windows.w_suc_payment(),
            windows.w_question_input()
        ),
        Dialog(
            windows.order_page()
        ),
        Dialog(
            windows.send_doc_page(),
            windows.finish_doc_page()
        ),
        Dialog(
            windows.finish_course()
        )
    ]