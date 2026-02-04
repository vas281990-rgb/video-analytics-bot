import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()


class Settings:
    # Telegram
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")

    # Database
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")


settings = Settings()

# Fail fast if something critical is missing
if not settings.BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")
