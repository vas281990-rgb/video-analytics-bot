from typing import Literal
from pydantic import BaseModel
from datetime import date


class DateRange(BaseModel):
    date_from: date | None = None
    date_to: date | None = None


class QueryIntent(BaseModel):
    """
    Structured meaning of a natural language query.
    """

    metric: Literal[
        "count_videos",
        "count_videos_with_new_views",
        "sum_views_delta",
        "count_videos_by_views",
    ]

    creator_id: str | None = None
    min_views: int | None = None
    date_range: DateRange | None = None
    all_time: bool = False
