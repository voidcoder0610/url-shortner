## Day 1 — 17 September 2026
**Built:** Planned the URL shortener architecture on paper, mapped the write flow (shortening) and read flow (redirection), and initialized the Git repository structure with backend, frontend, and docs folders.
**Broke / debugged:** Clarified the difference between local Git tracking and remote GitHub hosting, navigated Windows PowerShell to run repository setup commands, and ensured the diagram was properly tracked in the `docs/` folder.
**Learned:** Explored how APIs and databases interact. Understood that while MD5 or random strings can generate collisions (requiring retry loops or collision checks), maintaining an auto-incrementing counter converted to Base62 mathematically guarantees unique short codes. Also learned how large-scale distributed systems use ZooKeeper to distribute ranges of counter tokens across multiple servers to prevent overlap and handle server failures.
**Open question:** How does PostgreSQL manage the auto-incrementing counter locally for our backend, and how will FastAPI talk to Postgres tomorrow?
**Prompt log:** None today (Day 1 was conceptual planning, architecture design, and repository setup).

## Day 2 — 20 September 2026
**Built:** Created the Python virtual environment (`venv`), configured dependencies in `requirements.txt`, and implemented `database.py` (Postgres connection engine) and `models.py` (SQLAlchemy ORM models for `Link` and `Click`).
**Broke / debugged:** Ran into Windows PATH issues where `python` wasn't recognized; resolved it by installing Python via the configuration manager and updating system environment variables. Worked through initial confusion around ORM syntax by breaking down the library/book analogy.
**Learned:** Why Redis (RAM) is placed in front of Postgres (Disk): high-traffic links can be read in microseconds from RAM without hammering the database disk on thousands of concurrent clicks. Also learned that a `ForeignKey` links click events to their parent link, enforcing referential integrity and preventing orphan data.
**Open question:** How will FastAPI use these models tomorrow to receive HTTP requests and turn them into database entries?
**Prompt log:** Generated `database.py` and `models.py` with the AI mentor using SQLAlchemy. Asked mentor for an analogy-driven breakdown of `ForeignKey` and `nullable=False` before committing the code.

## Day 3 — 23 September 2026
**Built:** Implemented Base62 encoder/decoder in `utils.py`, Redis cache helper in `cache.py`, Pydantic request/response schemas in `schemas.py`, and built both core endpoints: `POST /shorten` and `GET /r/{short_code}` in `routers/`. Tested live via Swagger UI docs and verified real browser redirects to Wikipedia.
**Broke / debugged:** Encountered `ModuleNotFoundError` because the virtual environment was inactive in a new terminal; diagnosed PowerShell execution policy restrictions and reactivated `venv`. Debugged unsaved file state (`main.py •`) and walked through mechanical line-by-line breakdown of chained SQLAlchemy queries.
**Learned:** Why HTTP 307 Temporary Redirect is essential for URL shorteners (prevents the browser from caching the redirect locally so our server can process every visit). Also learned how SQLAlchemy's `.query().filter().first()` returns `None` on missing records, allowing our `404 Not Found` guard to intercept invalid links cleanly.
**Open question:** How do we record click metadata (timestamp, referrer, country) to PostgreSQL in the background without adding any latency to the visitor's redirect?
**Prompt log:** Generated `utils.py`, `cache.py`, `schemas.py`, `routers/shorten.py`, `routers/redirect.py`, and `main.py`. Instructed mentor to explain all new syntax mechanically from left to right before moving forward.