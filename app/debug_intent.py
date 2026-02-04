from app.nlp.schemas import QueryIntent, DateRange

intent = QueryIntent(
    metric="count_videos",
    creator_id=42,
    date_range=DateRange(
        date_from="2024-01-01",
        date_to="2024-01-31",
    ),
)

print(intent)
