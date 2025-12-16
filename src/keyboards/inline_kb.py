# src/keyboards/inline_kb.py

from telebot import types
from src.config import SITE, COURSE_PAY_LINK, TRIAL_LECT, TRIAL_VIDEO


def main_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Приступить к занятиям", callback_data="start_course_flow"))
    kb.add(types.InlineKeyboardButton("Пройти пробный урок", callback_data="start_trial_flow"))
    kb.add(types.InlineKeyboardButton("Подробнее о программе и тарифах", callback_data="info_flow"))
    return kb


def pregnancy_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("До 12 недель", callback_data="term_0_12"))
    kb.add(types.InlineKeyboardButton("12–29 недель", callback_data="term_12_29"))
    kb.add(types.InlineKeyboardButton("30–38 недель", callback_data="term_30_38"))
    kb.add(types.InlineKeyboardButton("38+ недель", callback_data="term_38_plus"))
    return kb


def experience_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Нет, это первый опыт", callback_data="exp_none"))
    kb.add(types.InlineKeyboardButton("Немного пробовала", callback_data="exp_some"))
    kb.add(types.InlineKeyboardButton("Регулярно занимаюсь", callback_data="exp_regular"))
    return kb


def contra_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Все хорошо, противопоказаний нет", callback_data="contra_ok"))
    kb.add(types.InlineKeyboardButton("Есть противопоказания", callback_data="contra_yes"))
    kb.add(types.InlineKeyboardButton("Я не уверена", callback_data="contra_unsure"))
    return kb


def formats_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Комплексный курс (йога + лекции)", callback_data="fmt_course"))
    kb.add(types.InlineKeyboardButton("Индивидуальные занятия онлайн", callback_data="fmt_individual"))
    kb.add(types.InlineKeyboardButton("Консультация онлайн", callback_data="fmt_consult"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu"))
    return kb


def course_options_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Оплатить и начать заниматься", url=COURSE_PAY_LINK))
    kb.add(types.InlineKeyboardButton("Узнать подробнее", callback_data="course_info"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_formats"))
    return kb


def trial_lesson_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🎥 Видео-урок йоги", url=TRIAL_VIDEO))
    kb.add(types.InlineKeyboardButton("🎧 Лекция «Подготовка к родам»", url=TRIAL_LECT))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu"))
    return kb


def prepayment_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Внести предоплату", url=COURSE_PAY_LINK))
    kb.add(types.InlineKeyboardButton("Пройти пробный урок", callback_data="flow_trial"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="flow_info"))
    return kb
