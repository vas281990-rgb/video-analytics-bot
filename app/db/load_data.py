import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from app.db.session import AsyncSessionLocal
from app.db.models import Video, VideoSnapshot


def uuid_to_int(value: str) -> int:
    """
    Convert UUID-like string to a stable positive integer.
    Same input -> same output every time.
    """
    return abs(hash(value))


# Path to source JSON file
JSON_PATH = Path("data/videos.json")


def parse_datetime(value: str) -> datetime:
    """
    Parse ISO datetime string into timezone-aware UTC datetime.

    JSON gives strings like:
    2025-11-26T11:00:08.983295Z

    DB expects real datetime objects with timezone.
    """
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))

    # Force UTC timezone (safety net)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(timezone.utc)


async def load_data() -> None:
    """
    Load videos and hourly snapshots from JSON into PostgreSQL.

    Think of this as carefully unpacking boxes into a warehouse 📦
    """
    async with AsyncSessionLocal() as session:
        with JSON_PATH.open(encoding="utf-8") as f:
            payload = json.load(f)

        videos = payload["videos"]

        for video in videos:
            video_id = uuid_to_int(video["id"])

            video_obj = Video(
                id=video_id,
                creator_id=uuid_to_int(video["creator_id"]),
                video_created_at=parse_datetime(video["created_at"]),
                views_count=video["views_count"],
                likes_count=video["likes_count"],
                comments_count=video["comments_count"],
                reports_count=video["reports_count"],
            )

            session.add(video_obj)

            for snap in video["snapshots"]:
                snapshot_obj = VideoSnapshot(
                    video_id=video_id,
                    views_count=snap["views_count"],
                    likes_count=snap["likes_count"],
                    comments_count=snap["comments_count"],
                    reports_count=snap["reports_count"],
                    delta_views_count=snap["delta_views_count"],
                    delta_likes_count=snap["delta_likes_count"],
                    delta_comments_count=snap["delta_comments_count"],
                    delta_reports_count=snap["delta_reports_count"],
                    created_at=parse_datetime(snap["created_at"]),
                )

                session.add(snapshot_obj)

        await session.commit()

    print("✅ JSON data successfully loaded into database")


if __name__ == "__main__":
    asyncio.run(load_data())
