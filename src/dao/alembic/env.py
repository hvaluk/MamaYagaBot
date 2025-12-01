import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Добавляем src в sys.path, чтобы Alembic мог импортировать модели
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Импортируем Base и engine из твоего models.py
from src.dao.models import Base, engine

# Alembic config
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Для autogenerate
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.getenv("MAMAYOGA_DATABASE_URL", "sqlite:///mamayoga_bot.db")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine  # используем engine из models.py

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Выбор режима
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
