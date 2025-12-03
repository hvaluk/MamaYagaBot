# src/handlers/booking.py
from telebot import types
from src.common import bot
from src.dao import crud
from src.config import PAY_LINK

USER_STATE = {}

def set_state(user_id, state):
    USER_STATE[user_id] = state

def pop_state(user_id):
    return USER_STATE.pop(user_id, None)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("book_"))
async def cb_book_format(call):
    await bot.answer_callback_query(call.id)
    fmt = call.data.split("_", 1)[1]
    user_id = call.from_user.id
    set_state(user_id, {"step": "await_payment_or_contact", "format": fmt})

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Оплатить картой", url=PAY_LINK))
    kb.add(types.InlineKeyboardButton("Я оплатил(а), отправить контакт", callback_data=f"paid_{fmt}"))

    await bot.send_message(call.message.chat.id,
                           f"Вы выбрали: {fmt}.\nОплатите по ссылке или нажмите «Я оплатил(а)» и отправьте контакт.",
                           reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("paid_"))
async def cb_paid(call):
    await bot.answer_callback_query(call.id, "Спасибо! Заявка сохранена.")
    fmt = call.data.split("_",1)[1]
    user_id = call.from_user.id
    await crud.create_request(user_id, "payment", format_chosen=fmt, payload="paid_via_link", followup_hours=24)
    await bot.send_message(call.message.chat.id, "Спасибо! Анна получила вашу заявку и скоро свяжется с вами.")

@bot.message_handler(content_types=["contact", "text"])
async def receive_contact_or_text(message):
    user_id = message.from_user.id
    state = USER_STATE.get(user_id)
    if message.contact and getattr(message.contact, "phone_number", None):
        phone = message.contact.phone_number
    else:
        phone = (message.text or "").strip()

    if state and state.get("step") == "await_payment_or_contact":
        fmt = state.get("format")
        await crud.upsert_user_contact(user_id, phone)
        await crud.create_request(user_id, "booking", format_chosen=fmt, payload=phone, followup_hours=24)
        pop_state(user_id)
        await bot.send_message(message.chat.id, "Спасибо! Анна получила вашу заявку и скоро свяжется с вами.")
    else:
        return
