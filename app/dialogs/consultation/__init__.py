from aiogram_dialog import Dialog

from . import consul_window

def consul_menu_dialog():
    return [
        Dialog(
            consul_window.consul_quiz(),
            consul_window.w_cosultation(),
            consul_window.finish_quiz_window(),
            consul_window.send_order()
        ),
    ]