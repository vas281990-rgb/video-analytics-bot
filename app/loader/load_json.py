import json
from pathlib import Path
from datetime import datetime

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Video, VideoSnapshot
from app.db.session import AsyncSessionLocal


# Path to videos.json in project root
JSON_PATH = Path(__file__).resolve().parents[2] / "videos.json"


def parse_datetime(value: str) -> datetime:
    """
    Parse ISO datetime string to datetime object
    """
    return datetime.fromisoformat(value)


async def load_data() -> None:
    """
    Load videos and snapshots from JSON file into database
    """
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    videos = data["videos"]

    async with AsyncSessionLocal() as session:  
        async with session.begin():
            for video in videos:
                video_row = {
                    "id": video["id"],
                    "creator_id": video["creator_id"],
                    "video_created_at": parse_datetime(video["video_created_at"]),
                    "views_count": video["views_count"],
                    "likes_count": video["likes_count"],
                    "comments_count": video["comments_count"],
                    "reports_count": video["reports_count"],
                }

                await session.execute(
                    insert(Video).values(**video_row)
                )

                snapshots_rows = []
                for snapshot in video["snapshots"]:
                    snapshots_rows.append(
                        {
                            "id": snapshot["id"],
                            "video_id": video["id"],
                            "views_count": snapshot["views_count"],
                            "likes_count": snapshot["likes_count"],
                            "comments_count": snapshot["comments_count"],
                            "reports_count": snapshot["reports_count"],
                            "delta_views_count": snapshot["delta_views_count"],
                            "delta_likes_count": snapshot["delta_likes_count"],
                            "delta_comments_count": snapshot["delta_comments_count"],
                            "delta_reports_count": snapshot["delta_reports_count"],
                            "created_at": parse_datetime(snapshot["created_at"]),
                        }
                    )

                if snapshots_rows:
                    await session.execute(
                        insert(VideoSnapshot).values(snapshots_rows)
                    )

        await session.commit()


if __name__ == "__main__":
    import asyncio

    asyncio.run(load_data())
