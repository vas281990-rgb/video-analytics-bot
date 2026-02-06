import re
from datetime import date, datetime
from app.nlp.schemas import QueryIntent, DateRange

class NLPParser:
    
    MONTHS_MAP = {
        "янв": 1, "фев": 2, "мар": 3, "апр": 4, "май": 5, "июн": 6,
        "июл": 7, "авг": 8, "сен": 9, "окт": 10, "ноя": 11, "дек": 12
    }

    async def parse(self, text: str) -> QueryIntent:
        text = text.lower()
        
        metric = "count_videos"
        if "прирост" in text or "выросли" in text:
            metric = "sum_views_delta"
        elif "новые просмотры" in text or "получали новые просмотры" in text:
            metric = "count_videos_with_new_views"
        elif "больше" in text and "просмотров" in text:
            metric = "count_videos_by_views"

        # 2. Ищем Creator ID и Min Views (оставляем как было)
        creator_id = None
        match_id = re.search(r"id\s*([a-f0-9]+)", text) # Ищем hex-строку
        if match_id:
            creator_id = match_id.group(1)

        min_views = None
        match_views = re.search(r"больше\s+([\d\s]+)", text)
        if match_views:
            min_views = int(match_views.group(1).replace(" ", ""))

        date_range = self._extract_date_range(text)

        return QueryIntent(
            metric=metric,
            creator_id=creator_id,
            min_views=min_views,
            date_range=date_range,
            all_time="все время" in text
        )

    def _extract_date_range(self, text: str) -> DateRange:

        date_pattern = r"(\d{1,2})\s+([а-я]{3,})\s+(\d{4})"
        dates = re.findall(date_pattern, text)
        
        extracted_dates = []
        for d, m, y in dates:
            month_num = 11 
            for name, num in self.MONTHS_MAP.items():
                if name in m:
                    month_num = num
                    break
            extracted_dates.append(date(int(y), month_num, int(d)))

        if len(extracted_dates) >= 2:
            return DateRange(date_from=extracted_dates[0], date_to=extracted_dates[1])
        elif len(extracted_dates) == 1:
            return DateRange(date_from=extracted_dates[0], date_to=extracted_dates[0])
        
        return None
