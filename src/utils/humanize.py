# src/utils/humanize.py

TERM_MAP = {
    "до 12 недель": "До 12 недель",
    "12–29 недель": "12–29 недель",
    "30–38 недель": "30–38 недель",
    "38+ недель": "38+ недель",
}

EXP_MAP = {
    "нет": "Не занималась",
    "немного": "Немного пробовала",
    "регулярно": "Регулярно занимаюсь",
}

CONTRA_MAP = {
    "contra_ok": "Противопоказаний нет",
    "contra_yes": "Есть противопоказания",
    "contra_unsure": "Не уверена",
}

FORMAT_MAP = {
    "fmt_course": "Йога онлайн в группе",
    "fmt_individual": "Индивидуальные занятия",
    "fmt_consult": "Консультация онлайн",
    "not_chosen": "Не выбран"
}


def humanize(value: str | None, mapping: dict) -> str:
    """
    Преобразует кодовое значение в человекочитаемую строку по словарю mapping.
    Для FORMAT_MAP: если значение "contra" или None -> "Не выбран"
    """
    if value is None:
        return "—"
    
    if mapping == FORMAT_MAP and value in ("contra", None):
        return "Не выбран"
    
    return mapping.get(value, value)
