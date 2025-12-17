# MamaYagaBot 
# MamaYogaBot (async SQLite version)

## Setup
1. Create venv and install deps:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Copy example .env:
   cp .env.example .env
   Fill TELEGRAM_TOKEN and ADMIN_IDS

3. Run bot:
   python -m src.main

## Alembic migrations
From project root:
   alembic -c alembic.ini revision --autogenerate -m "init"
   alembic -c alembic.ini upgrade head



| callback_data       | handler               | описание         |
| ------------------- | --------------------- | ---------------- |
| `start_course_flow` | `start_course`        | старт сценария   |
| `term_0_12`         | `save_pregnancy_term` | срок             |
| `term_12_29`        | `save_pregnancy_term` | срок             |
| `term_30_38`        | `save_pregnancy_term` | срок             |
| `term_38_plus`      | `save_pregnancy_term` | срок             |
| `exp_none`          | `save_experience`     | опыт             |
| `exp_some`          | `save_experience`     | опыт             |
| `exp_regular`       | `save_experience`     | опыт             |
| `contra_ok`         | `save_contra`         | противопоказания |
| `contra_yes`        | `save_contra`         | противопоказания |
| `contra_unsure`     | `save_contra`         | противопоказания |
| `fmt_course`        | `full_course`         | выбор формата    |
| `course_pay`        | `course_pay`          | оплата           |
