from sqlalchemy import select, func, and_

from app.db.models import Video, VideoSnapshot
from app.nlp.schemas import QueryIntent


def build_query(intent: QueryIntent):
    """
    Convert structured intent into a SQLAlchemy query.

    Think of this function as a translator:
    human meaning → strict SQL logic 🧠➡️🧮
    """

    if intent.metric == "count_videos":
        return _count_videos(intent)

    if intent.metric == "count_videos_with_new_views":
        return _count_videos_with_new_views(intent)

    if intent.metric == "sum_views_delta":
        return _sum_views_delta(intent)

    if intent.metric == "count_videos_by_views":
        return _count_videos_by_views(intent)

    raise ValueError(f"Unknown metric: {intent.metric}")

def _count_videos(intent: QueryIntent):
    """
    Count videos with optional filters.
    """

    conditions = []

    if intent.creator_id is not None:
        conditions.append(Video.creator_id == intent.creator_id)

    if intent.date_range:
        if intent.date_range.date_from:
            conditions.append(Video.created_at >= intent.date_range.date_from)

        if intent.date_range.date_to:
            conditions.append(Video.created_at <= intent.date_range.date_to)

    query = select(func.count()).select_from(Video)

    if conditions:
        query = query.where(and_(*conditions))

    return query

def _count_videos_with_new_views(intent: QueryIntent):
    query = (
        select(func.count(func.distinct(VideoSnapshot.video_id)))
        .where(VideoSnapshot.delta_views_count > 0)
    )
    if intent.date_range:
        if intent.date_range.date_from:
            query = query.where(VideoSnapshot.created_at >= intent.date_range.date_from)
        if intent.date_range.date_to:
            query = query.where(VideoSnapshot.created_at <= intent.date_range.date_to)
    return query

def _sum_views_delta(intent: QueryIntent):
    query = select(func.coalesce(func.sum(VideoSnapshot.delta_views_count), 0))
    
    if intent.date_range:
        if intent.date_range.date_from:
            query = query.where(VideoSnapshot.created_at >= intent.date_range.date_from)
        if intent.date_range.date_to:
            query = query.where(VideoSnapshot.created_at <= intent.date_range.date_to)
    return query

def _count_videos_by_views(intent: QueryIntent):
    query = select(func.count()).select_from(Video)

    conditions = [Video.views_count >= intent.min_views]
    if intent.creator_id is not None:
        conditions.append(Video.creator_id == intent.creator_id)
    return query.where(and_(*conditions))
