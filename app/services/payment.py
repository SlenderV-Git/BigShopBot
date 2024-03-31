from aiogram import Bot
from aiogram.types import Message, LabeledPrice
from app.dialogs.main_dialog.lexicon import ORDERS
from app.config_reader import load_setting

def make_price(label, price):
    return LabeledPrice(label=label, amount=price)

async def send_order(message : Message, order_name : str, price : int, **kwargs):
    order = ORDERS[order_name]
    payload = order["payload"]
    param = kwargs.get("course_id")
    if param:
        payload += f"_{param}"
    await message.bot.send_invoice(
        chat_id= message.chat.id,
        title= order["title"],
        description=order["description"],
        payload=payload,
        provider_token=load_setting().provider_token,
        prices=[make_price(order["prices"], price=price * 100)],
        currency=order["currency"],
        photo_url=order["photo"]
    )
    