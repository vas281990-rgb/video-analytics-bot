from sqlalchemy import text


def build_sql_query(user_text: str):
    """
    Convert a natural language question (RU)
    into a deterministic SQL query.

    Always returns SQLAlchemy text() object.
    """

    text_lower = user_text.lower()


    if "сколько" in text_lower and "видео" in text_lower:
        return text("SELECT COUNT(*) FROM videos")

    if "сколько" in text_lower and "снапшот" in text_lower:
        return text("SELECT COUNT(*) FROM video_snapshots")

    if "максимум" in text_lower and "просмотр" in text_lower:
        return text("SELECT MAX(views_count) FROM video_snapshots")

    if "минимум" in text_lower and "просмотр" in text_lower:
        return text("SELECT MIN(views_count) FROM video_snapshots")

    raise ValueError("Unrecognized analytics query")