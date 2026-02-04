from app.nlp.schemas import QueryIntent


class NLPParser:
    """
    Converts natural language (Russian) into structured QueryIntent.

    For now this is a stub.
    Later it will be powered by an LLM 🧠
    """

    async def parse(self, text: str) -> QueryIntent:
        """
        Parse user message into a QueryIntent.

        One input → one intent → one SQL query.
        """

        text = text.lower()

        # Temporary hardcoded rules for smoke testing
        if "сколько всего видео" in text:
            return QueryIntent(metric="count_videos")

        if "больше" in text and "просмотров" in text:
            return QueryIntent(
                metric="count_videos_by_views",
                min_views=100_000,
            )

        raise ValueError("Cannot parse user query yet")
