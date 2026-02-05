from datetime import date
from app.nlp.schemas import QueryIntent, DateRange
from app.db.queries import build_query


intent = QueryIntent(
    metric="count_videos",
    creator_id=42,
    date_range=DateRange(
        date_from=date(2024, 1, 1),
        date_to=date(2024, 1, 31),
    )
)

query = build_query(intent)

print(query)
