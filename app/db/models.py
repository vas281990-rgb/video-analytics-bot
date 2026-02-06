from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key=True)
    creator_id = Column(String, index=True, nullable=False)

    # Store original video creation time in UTC (timezone-aware)
    video_created_at = Column(
        DateTime(timezone=True),
        index=True,
        nullable=False,
    )

    views_count = Column(BigInteger, nullable=False)
    likes_count = Column(BigInteger, nullable=False)
    comments_count = Column(BigInteger, nullable=False)
    reports_count = Column(BigInteger, nullable=False)

    # Timestamps managed by DB, always in UTC
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    snapshots = relationship("VideoSnapshot", back_populates="video")


class VideoSnapshot(Base):
    __tablename__ = "video_snapshots"
    id = Column(Integer, primary_key=True)
    video_id = Column(
        String,
        ForeignKey("videos.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    views_count = Column(BigInteger, nullable=False)
    likes_count = Column(BigInteger, nullable=False)
    comments_count = Column(BigInteger, nullable=False)
    reports_count = Column(BigInteger, nullable=False)

    delta_views_count = Column(BigInteger, nullable=False)
    delta_likes_count = Column(BigInteger, nullable=False)
    delta_comments_count = Column(BigInteger, nullable=False)
    delta_reports_count = Column(BigInteger, nullable=False)

    # Snapshot timestamp, must be timezone-aware (UTC)
    created_at = Column(
        DateTime(timezone=True),
        index=True,
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    video = relationship("Video", back_populates="snapshots")


# Helpful indexes for analytics queries
Index("ix_snapshots_created_at", VideoSnapshot.created_at)
Index("ix_videos_views_count", Video.views_count)
