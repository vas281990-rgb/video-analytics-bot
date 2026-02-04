from pydantic_settings import BaseSettings
from pydantic import computed_field


class Settings(BaseSettings):
    # Database settings

    DB_HOST: str = "localhost"
    DB_PORT: int = 5433
    DB_NAME: str = "video_analytics"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    # Telegram bot
    BOT_TOKEN: str = "8422258435:AAHAKj3w-udaZhy7o9fL4t9bJcTNw7Eui4U"

    # LLM (optional, later)

    LLM_API_KEY: str | None = None

    # Computed values

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Build async PostgreSQL URL for SQLAlchemy.
        Like assembling a Lego spaceship from parts 🧱🚀
        """
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
