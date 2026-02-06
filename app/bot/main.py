import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

from app.db.session import AsyncSessionLocal
from app.services.analytics import build_sql_query
from app.nlp.parser import NLPParser
from app.db.queries import build_query

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
parser = NLPParser()


@dp.message(F.text)
async def handle_message(message: Message):
    """
    Main message handler.
    """
    user_text = message.text.strip()

    try:
        intent = await parser.parse(user_text)
        query = build_sql_query(user_text)

        async with AsyncSessionLocal() as session:
            result = await session.execute(query)
            value = result.scalar()

        await message.answer(str(value if value is not None else o))

    except Exception as exc:
        logging.exception(exc)
        await message.answer(
            "Не смог понять запрос 😔\n"
            "Попробуй сформулировать иначе."
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
