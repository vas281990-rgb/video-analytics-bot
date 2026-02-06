# Video Analytics Telegram Bot

An asynchronous Telegram bot for analytics of video creators data.

The bot accepts natural language queries in Russian and always returns exactly one numeric value, calculated by a deterministic SQL query executed against a PostgreSQL database.

This project was implemented as a technical test task with a strong focus on:

- Predictability — same input always yields the same result  
- Reliability — zero hallucinations, fully controlled logic  
- Determinism — no hidden state, no dialogue context  
- Performance — fully async architecture (aiogram + SQLAlchemy)

---

##  Functional constraints (from the task)

This solution strictly follows the task requirements:

-  no conversational context
-  no follow-up questions
-  no textual explanations
-  one request → one SQL query → one numeric answer
-  deterministic behavior

Each user message is processed independently.

---

##  What the bot can do

- Count total number of videos in the system
- Aggregate metrics:
  - views
  - likes
  - comments
  - reports
- Analyze metric deltas over time (growth / decline)
- Filter data by:
  - creator ID
  - publication date ranges
  - numeric thresholds

---

##  Key design decision: no LLM

Although the task allows using LLMs, this solution intentionally does not use any LLM.

Reasons:
- The database schema is fixed and known in advance
- Queries must be precise and reproducible
- Any hallucination or ambiguity would reduce trust in analytics

Instead, the bot uses a fully deterministic NLP pipeline based on regular expressions and explicit rules.

This guarantees:
- same input → same SQL → same result
- predictable behavior
- easy debugging and validation

---

##  Architecture overview

The request processing pipeline is split into clear, isolated stages:

### 1. NLP Parsing
User input is parsed by a deterministic NLP parser:
- extracts metric type (count, sum, delta)
- detects creator IDs
- parses date ranges and numeric thresholds

The output of this stage is a structured QueryIntent object.

### 2. SQL Query Building
QueryIntent is converted into a SQLAlchemy Core expression:
- no raw SQL strings
- explicit joins and filters
- controlled aggregation logic

### 3. Execution
The query is executed using async SQLAlchemy with PostgreSQL.
The resulting scalar value is returned to the user.

---

##  Database

- PostgreSQL
- Two main tables:
  - videos
  - video_snapshots (hourly metrics)

Indexes are added for:
- time-based analytics
- aggregation performance

---

##  Example queries

Each query produces exactly one numeric response.

---

##  Loading initial data (JSON)

Clone the repository and create a .env file based on .env.example:

```bash
cp .env.example .env
python -m app.db.load_data

Running the Bot

python -m app.bot.main