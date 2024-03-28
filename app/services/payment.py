from aiogram import Bot
from aiogram.types import Message, LabeledPrice
from app.dialogs.main_dialog.lexicon import ORDERS
from app.config_reader import load_setting

def make_price(price_raw : tuple):
    return [LabeledPrice(label=price[0].format(load_setting().top_up), amount=price[1]) for price in price_raw]

async def send_order(message : Message, bot : Bot, order_name : str):
    order = ORDERS[order_name]
    await bot.send_invoice(
        chat_id= message.chat.id,
        title= order["title"],
        description=order["description"],
        payload=order["payload"],
        provider_token=load_setting().provider_token,
        prices=make_price(order["prices"]),
        currency=order["currency"],
        photo_url=order["photo"]
    )