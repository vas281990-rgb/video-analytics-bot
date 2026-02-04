import asyncio
import json
from datetime import datetime
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.db.models import Video, VideoSnapshot


JSON_PATH = Path("data/videos.json")


def parse_datetime(value: str) -> datetime:
    """
    Parse ISO datetime string into Python datetime.
    JSON gives us strings, DB wants real time ⏳
    """
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


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
            video_obj = Video(
                id=video["id"],
                creator_id=video["creator_id"],
                video_created_at=parse_datetime(video["video_created_at"]),
                views_count=video["views_count"],
                likes_count=video["likes_count"],
                comments_count=video["comments_count"],
                reports_count=video["reports_count"],
            )

            session.add(video_obj)

            for snap in video["snapshots"]:
                snapshot_obj = VideoSnapshot(
                    video_id=video["id"],
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
