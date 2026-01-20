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
    if not value:
        return "—"
    return mapping.get(value, value)
