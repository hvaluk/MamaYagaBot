# src/keyboards/inline_kb.py

from telebot import types
from src.config import COURSE_PAY_LINK


# ---------------- Главная клавиатура после /start ----------------
def main_kb():
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("Записаться", callback_data="start_course_flow"),
        types.InlineKeyboardButton("Пробный урок", callback_data="flow_trial_start"),
    )
    kb.add(
        types.InlineKeyboardButton(
            "Подробнее о программе и тарифах",
            callback_data="flow_info"
        )
    )
    return kb


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
    return kb


# ---------------- Опции для Йога онлайн в группе ----------------
def course_options_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Оплатить и начать заниматься", url=COURSE_PAY_LINK))
    kb.add(types.InlineKeyboardButton("Узнать подробнее", callback_data="flow_course_info"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb


# ---------------- Подробная информация о курсе ----------------
def course_info_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Оплатить и начать заниматься", url=COURSE_PAY_LINK))
    kb.add(types.InlineKeyboardButton("Пройти пробный урок", callback_data="flow_trial"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb


# ---------------- Индивидуальные занятия ----------------
def individual_options_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Начать заниматься", callback_data="start_individual"))
    kb.add(types.InlineKeyboardButton("Узнать подробнее", callback_data="individual_info"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb


# ---------------- Подробная информация об индивидуальных занятиях ----------------
def individual_info_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Начать заниматься", callback_data="start_individual"))
    kb.add(types.InlineKeyboardButton(
        "Записаться на бесплатное мини-занятие",
        callback_data="flow_trial"
    ))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb


# ---------------- Консультация ----------------
def consult_options_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Записаться", callback_data="start_consultation"))
    kb.add(types.InlineKeyboardButton("Пройти пробный урок", callback_data="flow_trial"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb


# ---------------- Пробный урок ----------------
def trial_lesson_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🎥 Видео-урок йоги", callback_data="trial_video"))
    kb.add(types.InlineKeyboardButton("🎧 Лекция «Подготовка к родам»", callback_data="trial_lect"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb


# ---------------- Подробная информация о курсе (из главного меню) ----------------
def course_flow_info_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Оплатить и начать заниматься", url=COURSE_PAY_LINK))
    kb.add(types.InlineKeyboardButton("Пройти пробный урок", callback_data="flow_trial_start"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb



def followup_60min_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("🔹Оплатить и начать заниматься", url=COURSE_PAY_LINK),
        types.InlineKeyboardButton("🔹Подробнее о программе и тарифах", callback_data="flow_info")
    )
    return kb

def followup_24h_kb():  
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("🔸Хочу записаться на курс", url=COURSE_PAY_LINK),
        types.InlineKeyboardButton("🔸Есть вопросы", callback_data="contact_request"),
        types.InlineKeyboardButton("🔸Напомни позже", callback_data="remind_later")
    )
    return kb