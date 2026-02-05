import re
from datetime import date, datetime

from app.nlp.schemas import QueryIntent, DateRange


class NLPParser:
    """
    Deterministic parser:
    Russian text → structured QueryIntent.
    """

    async def parse(self, text: str) -> QueryIntent:
        text = text.lower()

        # -----------------------
        # 1. Определяем metric
        # -----------------------

        if "прирост" in text or "выросли" in text:
            metric = "sum_views_delta"

        elif "новые просмотры" in text or "получали новые просмотры" in text:
            metric = "count_videos_with_new_views"

        elif "больше" in text and "просмотров" in text:
            metric = "count_videos_by_views"

        elif "сколько" in text and "видео" in text:
            metric = "count_videos"

        else:
            raise ValueError("Cannot detect metric")

        # -----------------------
        # 2. Creator ID
        # -----------------------

        creator_id = None
        match = re.search(r"id\s*(\d+)", text)
        if match:
            creator_id = int(match.group(1))

        # -----------------------
        # 3. Минимальные просмотры
        # -----------------------

        min_views = None
        match = re.search(r"больше\s+([\d\s]+)", text)
        if match:
            min_views = int(match.group(1).replace(" ", ""))

        # -----------------------
        # 4. Даты
        # -----------------------

        date_range = None
        all_time = False

        if "за всё время" in text or "за все время" in text:
            all_time = True

        # формат: 27 ноября 2025
        match = re.search(
            r"(\d{1,2})\s+(ноября|ноябрь)\s+(\d{4})", text
        )
        if match:
            day, _, year = match.groups()
            d = date(int(year), 11, int(day))
            date_range = DateRange(date_from=d, date_to=d)

        # формат: с 1 ноября 2025 по 5 ноября 2025
        match = re.search(
            r"с\s+(\d{1,2})\s+ноября\s+(\d{4}).*по\s+(\d{1,2})\s+ноября\s+(\d{4})",
            text,
        )
        if match:
            d1, y1, d2, y2 = match.groups()
            date_range = DateRange(
                date_from=date(int(y1), 11, int(d1)),
                date_to=date(int(y2), 11, int(d2)),
            )

        return QueryIntent(
            metric=metric,
            creator_id=creator_id,
            min_views=min_views,
            date_range=date_range,
            all_time=all_time,
        )