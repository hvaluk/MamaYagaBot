# src/utils/humanize.py
import datetime 

TERM_MAP = {
    "term_0_12": "До 12 недель",
    "term_12_29": "12–29 недель",
    "term_30_38": "30–38 недель",
    "term_38_plus": "38+ недель",
}

EXP_MAP = {
    "exp_none": "нет",
    "exp_some": "немного",
    "exp_regular": "регулярно",
}

CONTRA_MAP = {
    "contra_ok": "Противопоказаний нет",
    "contra_yes": "Есть противопоказания",
    "contra_unsure": "Не уверена",
}

FORMAT_MAP = {
    "fmt_course": "Йога онлайн в группе",
    "fmt_individual": "Индивидуальные занятия",
    "fmt_consult": "Мини-консультация онлайн",
    "not_chosen": "Не выбран"
}

FEELING_MAP = {
    "feeling_tension": "Есть напряжение в теле (спина, таз, шея)",
    "feeling_anxiety": "Часто тревожно / много мыслей",
    "feeling_tired": "Бывает усталость, нет сил",
    "feeling_good": "В целом всё хорошо, но хочу подготовиться к родам",
}

REQUEST_MAP = {
    "request_prepare_birth": "Подготовиться к родам",
    "request_relieve_tension": "Убрать напряжение в теле",
    "request_learn_relax": "Научиться расслабляться",
    "request_guidelines": "Понять, что можно / нельзя",
}

def humanize(value: str | None, mapping: dict) -> str:
    """
     Convert an internal code to a human-readable label.
     
    """
    if value is None:
        return "—"
    
    if mapping == FORMAT_MAP and value in ("contra", None):
        return "Не выбран"
    
    return mapping.get(value, value)

def format_human_datetime(value) -> str:
    """
    Преобразует timestamp (float или ISO str) в красивую дату
    """
    if value is None:
        return "—"
    
    # если пришёл float (UNIX timestamp)
    if isinstance(value, (float, int)):
        try:
            dt = datetime.datetime.fromtimestamp(value)
            return dt.strftime("%d.%m.%Y %H:%M")
        except Exception:
            return str(value)
    
    # если уже строка ISO
    if isinstance(value, str):
        try:
            dt = datetime.datetime.fromisoformat(value)
            return dt.strftime("%d.%m.%Y %H:%M")
        except Exception:
            return value
    
    return str(value)