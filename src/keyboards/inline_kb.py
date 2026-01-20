# src/keyboards/inline_kb.py

from telebot import types
from src.config import COURSE_PAY_LINK, TRIAL_LECT, TRIAL_VIDEO

# ---------------- Главная клавиатура после /start ----------------
def main_kb():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Записаться", callback_data="start_course_flow")
    btn2 = types.InlineKeyboardButton("Пробный урок", callback_data="flow_trial")
    markup.row(btn1, btn2)

    btn3 = types.InlineKeyboardButton("Подробнее о программе и тарифах", callback_data="flow_info")
    markup.row(btn3)
    return markup

# ---------------- Выбор срока беременности ----------------
def pregnancy_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("До 12 недель", callback_data="term_0_12"))
    kb.add(types.InlineKeyboardButton("12–29 недель", callback_data="term_12_29"))
    kb.add(types.InlineKeyboardButton("30–38 недель", callback_data="term_30_38"))
    kb.add(types.InlineKeyboardButton("38+ недель", callback_data="term_38_plus"))
    return kb

# ---------------- Опыт занятий йогой ----------------
def experience_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Нет, это первый опыт", callback_data="exp_none"))
    kb.add(types.InlineKeyboardButton("Немного пробовала", callback_data="exp_some"))
    kb.add(types.InlineKeyboardButton("Регулярно занимаюсь", callback_data="exp_regular"))
    return kb

# ---------------- Противопоказания ----------------
def contra_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Все хорошо, противопоказаний нет", callback_data="contra_ok"))
    kb.add(types.InlineKeyboardButton("Есть противопоказания", callback_data="contra_yes"))
    kb.add(types.InlineKeyboardButton("Я не уверена", callback_data="contra_unsure"))
    return kb

# ---------------- Выбор формата курса ----------------
def formats_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Йога онлайн в группе", callback_data="fmt_course"))
    kb.add(types.InlineKeyboardButton("Индивидуальные занятия онлайн", callback_data="fmt_individual"))
    kb.add(types.InlineKeyboardButton("Консультация онлайн", callback_data="fmt_consult"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu"))
    return kb

# ---------------- Опции для Йога онлайн в группе ----------------
def course_options_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Оплатить и начать заниматься", url=COURSE_PAY_LINK))
    kb.add(types.InlineKeyboardButton("Узнать подробнее", callback_data="flow_course_info"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_formats"))
    return kb
# ---------------- Подробная информация о курсе ----------------
def course_info_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Оплатить и начать заниматься", url=COURSE_PAY_LINK))
    kb.add(types.InlineKeyboardButton("Пройти пробный урок", callback_data="flow_trial"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_formats"))
    return kb

# ---------------- Индивидуальные занятия ----------------
def individual_options_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Начать заниматься", callback_data="start_individual"))
    kb.add(types.InlineKeyboardButton("Узнать подробнее", callback_data="individual_info"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_formats"))
    return kb

# ---------------- Консультация ----------------
def consult_options_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Записаться", callback_data="contact_request"))
    kb.add(types.InlineKeyboardButton("Пройти пробный урок", callback_data="flow_trial"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_formats"))
    return kb

# ---------------- Пробный урок ----------------
def trial_lesson_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🎥 Видео-урок йоги", url=TRIAL_VIDEO))
    kb.add(types.InlineKeyboardButton("🎧 Лекция «Подготовка к родам»", url=TRIAL_LECT))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_formats"))
    return kb

# ---------------- Предоплата ----------------
def prepayment_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Внести предоплату", url=COURSE_PAY_LINK))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="flow_info"))
    return kb

# ---------------- Отправка контакта ----------------
def contact_request_kb():  # Используется для индивидуальных занятий и консультации
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(types.KeyboardButton(text="Отправить номер телефона", request_contact=True))
    return kb
