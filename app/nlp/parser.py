import re
from datetime import date

from app.nlp.schemas import QueryIntent, DateRange


class NLPParser:
    """
    Deterministic parser:
    Russian text → structured QueryIntent.

    No context, no memory, no guessing.
    """

    async def parse(self, text: str) -> QueryIntent:
        text = text.lower()

        # 1. Metric detection
        if "сколько видео" in text:
            metric = "count_videos"
        elif "прирост просмотров" in text or "сумма просмотров" in text:
            metric = "sum_views_delta"
        elif "новые просмотры" in text:
            metric = "count_videos_with_new_views"
        elif "больше" in text and "просмотров" in text:
            metric = "count_videos_by_views"
        else:
            raise ValueError("Cannot detect metric")

        # 2. Creator ID
        creator_id = None
        match = re.search(r"автора\s+(\d+)", text)
        if match:
            creator_id = int(match.group(1))

        # 3. Min views threshold
        min_views = None
        match = re.search(r"больше\s+(\d+)", text)
        if match:
            min_views = int(match.group(1))

        # 4. Date range (very simple, deterministic)
        date_range = None
        if "январ" in text:
            date_range = DateRange(
                date_from=date(2024, 1, 1),
                date_to=date(2024, 1, 31),
            )

        return QueryIntent(
            metric=metric,
            creator_id=creator_id,
            min_views=min_views,
            date_range=date_range,
        )
