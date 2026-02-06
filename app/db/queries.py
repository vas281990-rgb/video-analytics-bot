from sqlalchemy import select, func, and_
from datetime import datetime, time, timezone

from app.db.models import Video, VideoSnapshot
from app.nlp.schemas import QueryIntent


def build_query(intent: QueryIntent):
    """
    Convert structured intent into a SQLAlchemy query.
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
    conditions = []

    if intent.creator_id is not None:
        conditions.append(Video.creator_id == intent.creator_id)

    if intent.date_range:
        if intent.date_range.date_from:
            date_from_dt = datetime.combine(
                intent.date_range.date_from,
                time.min,
                tzinfo=timezone.utc
            )
            conditions.append(Video.video_created_at >= date_from_dt)

        if intent.date_range.date_to:
            date_to_dt = datetime.combine(
                intent.date_range.date_to,
                time.max,
                tzinfo=timezone.utc
            )
            conditions.append(Video.video_created_at <= date_to_dt)

    query = select(func.count()).select_from(Video)

    if conditions:
        query = query.where(and_(*conditions))

    return query


def _count_videos_with_new_views(intent: QueryIntent):
    query = (
        select(func.count(func.distinct(VideoSnapshot.video_id)))
        .select_from(VideoSnapshot)
        .join(Video, Video.id == VideoSnapshot.video_id)
        .where(VideoSnapshot.delta_views_count > 0)
    )

    if intent.creator_id is not None:
        query = query.where(Video.creator_id == intent.creator_id)

    if intent.date_range:
        if intent.date_range.date_from:
            date_from_dt = datetime.combine(
                intent.date_range.date_from,
                time.min,
                tzinfo=timezone.utc
            )
            query = query.where(VideoSnapshot.created_at >= date_from_dt)

        if intent.date_range.date_to:
            date_to_dt = datetime.combine(
                intent.date_range.date_to,
                time.max,
                tzinfo=timezone.utc
            )
            query = query.where(VideoSnapshot.created_at <= date_to_dt)

    return query


def _sum_views_delta(intent: QueryIntent):
    query = select(func.coalesce(func.sum(VideoSnapshot.delta_views_count), 0))

    if intent.date_range:
        if intent.date_range.date_from:
            date_from_dt = datetime.combine(
                intent.date_range.date_from,
                time.min,
                tzinfo=timezone.utc
            )
            query = query.where(VideoSnapshot.created_at >= date_from_dt)

        if intent.date_range.date_to:
            date_to_dt = datetime.combine(
                intent.date_range.date_to,
                time.max,
                tzinfo=timezone.utc
            )
            query = query.where(VideoSnapshot.created_at <= date_to_dt)

    return query


def _count_videos_by_views(intent: QueryIntent):
    if intent.min_views is None:
        raise ValueError("min_views is required for count_videos_by_views")

    query = select(func.count()).select_from(Video)

    conditions = [
        Video.views_count > intent.min_views
    ]

    if intent.creator_id is not None:
        conditions.append(Video.creator_id == intent.creator_id)

    if intent.date_range:
        if intent.date_range.date_from:
            conditions.append(
                Video.video_created_at >= datetime.combine(
                    intent.date_range.date_from, time.min, tzinfo=timezone.utc
                )
            )
        if intent.date_range.date_to:
            conditions.append(
                Video.video_created_at <= datetime.combine(
                    intent.date_range.date_to, time.max, tzinfo=timezone.utc
                )
            )

    return query.where(and_(*conditions))
