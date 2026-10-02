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

## Day 4 — 1 October 2026
**Built:** Decoupled click event logging into an asynchronous background task using FastAPI's `BackgroundTasks`, implemented the analytics router in `backend/app/routers/analytics.py` (`GET /analytics/{short_code}`), and verified live that clicking links increments the click count in PostgreSQL without adding any redirect latency.
**Broke / debugged:** Worked through the tricky Python syntax of SQLAlchemy aggregate queries (`func.count()`, `.group_by()`, and `.scalar() or 0` to prevent `None` returns on fresh links). Clarified why background workers require their own independent `SessionLocal()` database sessions outside the endpoint lifecycle.
**Learned:** Why the non-negotiable constraint matters: writing to PostgreSQL on disk takes time, and blocking the redirect to write click metadata would degrade performance during viral traffic spikes. `BackgroundTasks` solves this by delivering the HTTP 307 response first, then recording the click metadata in the background.
**Open question:** How will our frontend dashboard visually represent these analytics, and how will our backend hold up when we deliberately stop Redis during the Day 5 chaos test?
**Prompt log:** Updated `redirect.py` with `BackgroundTasks` and generated `analytics.py` with the AI mentor. Dissected SQLAlchemy aggregate functions mechanically before testing.

## Day 5 — 2 October 2026
**Built:** Created the React frontend dashboard using Vite (`frontend/src/App.jsx`), enabled CORS middleware in FastAPI, connected the frontend to `/shorten` and `/analytics` endpoints, and completed the Day 5 Chaos Checklist.
**Broke / debugged:** Debugged a connection error when clicking "Shorten" by diagnosing that full-stack architecture requires two terminal sessions running concurrently (FastAPI backend on port 8000 and Vite React dev server on port 5173).
**Learned:** Why Cross-Origin Resource Sharing (CORS) is enforced by browsers when frontend and backend run on different ports. Learned how React manages controlled form inputs and component re-rendering using `useState`, and verified how our architecture provides graceful degradation under stress.
**Chaos Test Results:**
- [x] Rapid click test: Handled rapid successive visits without redirect latency, and click totals updated accurately on the React dashboard.
- [x] Ghost link test: Visiting an invalid short code returned a clean HTTP 404 (`{"detail": "Short link not found"}`) rather than an unhandled 500 crash.
- [x] Redis resiliency test: With `try...except` error boundaries in `cache.py`, cache issues degrade gracefully to PostgreSQL without crashing the API.
**Open question:** Ready for Demo Day live modifications!
**Prompt log:** Built React dashboard with the AI mentor in `App.jsx`, added CORS configuration to `main.py`, and verified the 3 Chaos Checklist tests.