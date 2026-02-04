from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    """
    /start command handler
    """
    await message.answer(
        "👋 Hi! I'm Video Analytics Bot.\n"
        "Send me a question about video analytics."
    )


@router.message()
async def text_handler(message: Message) -> None:
    """
    Catch-all text handler (temporary)
    """
    await message.answer("🤖 I received your message.")
