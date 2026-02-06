import asyncio
from app.db import models
from app.db.base import Base
from app.db.session import engine


async def init_db() -> None:
    """
    Create all database tables.

    Think of this as laying the foundation of a building 🏗️
    No tables → no data → no analytics.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database tables created successfully")


if __name__ == "__main__":
    asyncio.run(init_db())
