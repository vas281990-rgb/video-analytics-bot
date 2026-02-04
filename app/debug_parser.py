import asyncio
from app.nlp.parser import NLPParser


async def main():
    parser = NLPParser()

    intent = await parser.parse(
        "Сколько видео у автора 42 за январь"
    )

    print(intent)


if __name__ == "__main__":
    asyncio.run(main())
