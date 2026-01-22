# reset_db.py
import os
from sqlalchemy import create_engine
from src.dao.models import Base, DATABASE_URL
from alembic.config import Config
from alembic import command

# -------------------------
# Путь к базе SQLite
# -------------------------
DB_PATH = DATABASE_URL.replace("sqlite+aiosqlite:///", "")

# -------------------------
# Удаляем старую базу
# -------------------------
if os.path.exists(DB_PATH):
    print("Удаляем старую базу...")
    os.remove(DB_PATH)
else:
    print("Старой базы нет, пропускаем удаление.")

# -------------------------
# Создаём новую базу и все таблицы
# -------------------------
print("Создаём новую базу и все таблицы...")
engine = create_engine(DATABASE_URL.replace("+aiosqlite", ""))
Base.metadata.create_all(engine)
print("База создана.")

# -------------------------
# Настройка Alembic
# -------------------------
# Абсолютный путь к alembic.ini (в корне проекта)
ALEMBIC_INI_PATH = os.path.join(os.path.dirname(__file__), "alembic.ini")
alembic_cfg = Config(ALEMBIC_INI_PATH)

# Обновляем путь к папке миграций, если относительный
SCRIPT_LOCATION = os.path.join(os.path.dirname(__file__), "src", "dao", "alembic")
alembic_cfg.set_main_option("script_location", SCRIPT_LOCATION)

# -------------------------
# Отмечаем текущую схему как head
# -------------------------
command.stamp(alembic_cfg, "head")
print("Alembic обновлён, head установлен.")
