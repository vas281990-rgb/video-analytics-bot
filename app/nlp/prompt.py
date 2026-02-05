"""
This file documents the NLP contract used in the project.

Even though the current implementation uses a deterministic parser,
this prompt describes how an LLM could be instructed to produce
a valid QueryIntent without hallucinations.
"""

PROMPT_DESCRIPTION = """
You must convert a Russian analytical question into a JSON object
with the following structure:

QueryIntent:
- metric: one of:
    - count_videos
    - count_videos_with_new_views
    - sum_views_delta
    - count_videos_by_views
- creator_id: integer or null
- min_views: integer or null
- date_range:
    - date_from: YYYY-MM-DD or null
    - date_to: YYYY-MM-DD or null

Rules:
- Always return valid JSON
- Do not add extra fields
- If data is missing, use null
"""
