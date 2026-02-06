import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

from app.db.session import AsyncSessionLocal
from app.services.analytics import build_sql_query
from app.nlp.parser import NLPParser
from app.db.queries import build_query

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Load Telegram Bot token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
parser = NLPParser()


@dp.message(F.text)
async def handle_message(message: Message):
    """
    Main handler: processes natural language, executes SQL, and returns the result
    """
    user_text = message.text.strip()

    try:

        # Step 1: Parse natural language into a structured Intent
        intent = await parser.parse(user_text)

        # Step 2: Build SQLAlchemy query based on the Intent
        query = build_query(intent) 

        # Step 3: Execute query in PostgreSQL
        async with AsyncSessionLocal() as session:
            result = await session.execute(query)
            value = result.scalar()

        # Step 4: Send the numeric result back to the user
        await message.answer(str(value if value is not None else 0))

    except Exception as exc:
        logging.exception(exc)
        await message.answer(
            "Не смог понять запрос 😔\n"
            "Попробуй сформулировать иначе."
        )


async def main():
    # Start bot polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
