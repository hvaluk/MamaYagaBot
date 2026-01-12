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
   python3 main.py

## Alembic migrations
From project root:
   alembic -c alembic.ini upgrade head