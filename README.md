 # MamaYogaBot (Async Telegram bot with Grist as a database backend.)


1. Install dependencies (uv)
   uv sync

2. Copy example .env:
   cp .env.example .env
   Fill TELEGRAM_TOKEN and ADMIN_IDS
   GRIST_API_KEY,
   GRIST_DOC_ID,
   GRIST_URL

3. Run bot:
   uv run python main.py

