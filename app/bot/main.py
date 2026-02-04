import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from app.config.settings import settings
from app.db.session import AsyncSessionLocal
from app.db.queries import build_query
from app.nlp.parser import NLPParser

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

parser = NLPParser()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    """
    Simple /start command.
    """
    await message.answer(
        "Привет! Я бот для аналитики видео 📊\n"
        "Задай вопрос на русском — я отвечу числом."
    )


@dp.message()
async def analytics_handler(message: types.Message):
    """
    Main handler: one message → one numeric answer.
    """
    try:
        intent = await parser.parse(message.text)

        query = build_query(intent)

        async with AsyncSessionLocal() as session:
            result = await session.execute(query)
            value = result.scalar()

        # Always return a number
        await message.answer(str(value or 0))

    except Exception as exc:
        logging.exception(exc)
        await message.answer(
            "Не смог понять запрос 😔\n"
            "Попробуй сформулировать иначе."
        )


async def main():
    """
    Entry point for the Telegram bot.
    """
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
