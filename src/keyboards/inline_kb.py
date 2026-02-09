# src/keyboards/inline_kb.py

from telebot import types

# ---------------- Main keyboard after /start ----------------
def main_kb():
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("Записаться", callback_data="start_course_flow"),
        types.InlineKeyboardButton("Пробный мини-курс", callback_data="flow_trial_start"),
    )
    kb.add(
        types.InlineKeyboardButton(
            "Подробнее о программе и тарифах",
            callback_data="flow_info"
        )
    )
    return kb

# ---------------- Pregnancy term selection ----------------
def pregnancy_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("До 12 недель", callback_data="term_0_12"))
    kb.add(types.InlineKeyboardButton("12–29 недель", callback_data="term_12_29"))
    kb.add(types.InlineKeyboardButton("30–38 недель", callback_data="term_30_38"))
    kb.add(types.InlineKeyboardButton("38+ недель", callback_data="term_38_plus"))
    return kb

# ---------------- Yoga experience ----------------
def experience_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Нет, это первый опыт", callback_data="exp_none"))
    kb.add(types.InlineKeyboardButton("Немного пробовала", callback_data="exp_some"))
    kb.add(types.InlineKeyboardButton("Регулярно занимаюсь", callback_data="exp_regular"))
    return kb

# ---------------- Contraindications ----------------
def contra_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Все хорошо, противопоказаний нет", callback_data="contra_ok"))
    kb.add(types.InlineKeyboardButton("Есть противопоказания", callback_data="contra_yes"))
    kb.add(types.InlineKeyboardButton("Я не уверена", callback_data="contra_unsure"))
    return kb

# ---------------- Course format selection ----------------
def formats_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Йога онлайн в группе", callback_data="fmt_course"))
    kb.add(types.InlineKeyboardButton("Индивидуальные занятия онлайн", callback_data="fmt_individual"))
    kb.add(types.InlineKeyboardButton("Консультация онлайн", callback_data="fmt_consult"))
    return kb

# ---------------- Options for group online yoga ----------------
def course_options_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Оплатить и начать заниматься", callback_data="user:pay_course"))
    kb.add(types.InlineKeyboardButton("Узнать подробнее", callback_data="flow_course_info"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb

def course_info_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Оплатить и начать заниматься", callback_data="user:pay_course"))
    kb.add(types.InlineKeyboardButton("Пройти пробный мини-курс", callback_data="flow_trial"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb

def individual_options_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Начать заниматься", callback_data="start_individual"))
    kb.add(types.InlineKeyboardButton("Узнать подробнее", callback_data="individual_info"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb

def individual_info_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Начать заниматься", callback_data="start_individual"))
    kb.add(types.InlineKeyboardButton("Пройти пробный мини-курс", callback_data="flow_trial"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb

def consult_options_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Записаться", callback_data="start_consultation"))
    kb.add(types.InlineKeyboardButton("Пройти пробный мини-курс", callback_data="flow_trial"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb

def trial_lesson_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Мини-курс «Подготовка к родам»", callback_data="trial_lect"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb

def course_flow_info_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Оплатить и начать заниматься", callback_data="user:pay_course"))
    kb.add(types.InlineKeyboardButton("Пройти пробный мини-курс", callback_data="flow_trial_start"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
    return kb

# ---------------- Payment button via callback ----------------
def payment_confirm_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✅ Я оплатила", callback_data="user:paid"),
        types.InlineKeyboardButton("В меню", callback_data="back")
    )
    return kb

# ---------------- Follow-up keyboards ----------------
def followup_60min_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔹Оплатить и начать заниматься", callback_data="user:pay_course"))
    kb.add(types.InlineKeyboardButton("🔹Подробнее о программе и тарифах", callback_data="flow_info"))
    return kb

def followup_24h_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔸Хочу записаться на курс", callback_data="user:pay_course"))
    kb.add(types.InlineKeyboardButton("🔸Есть вопросы", callback_data="leave_contact"))
    kb.add(types.InlineKeyboardButton("🔸Напомни позже", callback_data="remind_later"))
    return kb

def followup_3days_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Записаться на курс", callback_data="user:pay_course"))
    kb.add(types.InlineKeyboardButton("Есть вопросы", callback_data="leave_contact"))
    return kb

# ---------------- Admin keyboards ----------------
def admin_request_kb(app_id: int):
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✔️ Выполнено", callback_data=f"admin:req_done:{app_id}"),
        types.InlineKeyboardButton("❌ Отклонено", callback_data=f"admin:req_reject:{app_id}")
    )
    return kb

def admin_payment_kb(app_id: int):
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✅ Оплачено", callback_data=f"admin:paid:{app_id}"),
        types.InlineKeyboardButton("❌ Не оплачено", callback_data=f"admin:not_paid:{app_id}")
    )
    return kb

def admin_main_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton(" Заявки", callback_data="admin:requests"),
        types.InlineKeyboardButton(" Оплаты", callback_data="admin:payments"), 
        types.InlineKeyboardButton(" Пользователи", callback_data="admin_users")
    )
    return kb
def admin_users_filter_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("Новые заявки", callback_data="admin_users:new"),
        types.InlineKeyboardButton("Ожидают оплаты", callback_data="admin_users:paid_pending")
    )
    kb.add(
        types.InlineKeyboardButton("Оплаченные", callback_data="admin_users:paid"),
        types.InlineKeyboardButton("На follow-up", callback_data="admin_users:followup")
    )
    kb.add(
        types.InlineKeyboardButton("🔙 Назад", callback_data="admin_main")
    )
    return kb
