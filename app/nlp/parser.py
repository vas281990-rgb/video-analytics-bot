import re
from datetime import date

from app.nlp.schemas import QueryIntent, DateRange


MONTHS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}


class NLPParser:
    """
    Deterministic parser:
    Russian text → structured QueryIntent.

    ⚠️ Без LLM
    ⚠️ Без контекста
    ⚠️ Только чёткие правила
    """

    async def parse(self, text: str) -> QueryIntent:
        text = text.lower()

        # 1. Определяем метрику

        if "сколько всего видео" in text or "сколько видео" in text:
            metric = "count_videos"

        if "больше" in text and "просмотров" in text:
            metric = "count_videos_by_views"

        if "прирост просмотров" in text or "на сколько просмотров" in text:
            metric = "sum_views_delta"

        if "новые просмотры" in text or "получали новые просмотры" in text:
            metric = "count_videos_with_new_views"

        # 2. Creator ID

        creator_id = None
        match = re.search(r"(креатора|автора)\s+id?\s*(\d+)", text)
        if match:
            creator_id = int(match.group(2))

        # 3. Минимум просмотров

        min_views = None
        match = re.search(r"больше\s+(\d+)", text)
        if match:
            min_views = int(match.group(1))

        # 4. Парсинг дат

        date_range = self._parse_dates(text)

        return QueryIntent(
            metric=metric,
            creator_id=creator_id,
            min_views=min_views,
            date_range=date_range,
        )

    def _parse_dates(self, text: str) -> DateRange | None:
        """
        Поддержка форм:
        - 28 ноября 2025
        - с 1 по 5 ноября 2025
        """

        # Диапазон: с 1 по 5 ноября 2025
        match = re.search(
            r"с\s+(\d{1,2})\s+по\s+(\d{1,2})\s+(\w+)\s+(\d{4})",
            text,
        )
        if match:
            day_from, day_to, month_word, year = match.groups()
            month = MONTHS.get(month_word)
            if month:
                return DateRange(
                    date_from=date(int(year), month, int(day_from)),
                    date_to=date(int(year), month, int(day_to)),
                )

        # Одна дата: 28 ноября 2025
        match = re.search(r"(\d{1,2})\s+(\w+)\s+(\d{4})", text)
        if match:
            day, month_word, year = match.groups()
            month = MONTHS.get(month_word)
            if month:
                d = date(int(year), month, int(day))
                return DateRange(date_from=d, date_to=d)

        return None
