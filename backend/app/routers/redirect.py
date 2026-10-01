from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.cache import get_cached_url, set_cached_url
from app.utils import decode_base62

router = APIRouter(tags=["Redirect"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def log_click_in_background(link_id: int, referrer: str | None, country: str | None):
    """
    Runs completely in the background AFTER the visitor is already redirected.
    Opens its own short-lived database session to record the event.
    """
    db = SessionLocal()
    try:
        click_record = models.Click(
            link_id=link_id,
            referrer=referrer,
            country=country
        )
        db.add(click_record)
        db.commit()
    except Exception as e:
        print(f"[CLICK LOG ERROR] Failed to record click for link {link_id}: {e}")
    finally:
        db.close()


@router.get("/r/{short_code}")
def redirect_to_long_url(
    short_code: str,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)
):
    # Extract visitor metadata from HTTP headers
    # Note: HTTP standard historically misspells 'referrer' as 'referer'
    referrer = request.headers.get("referer")
    country = request.headers.get("cf-ipcountry", "Unknown")

    # 1. Fast Path: Check Redis Cache (RAM)
    cached_url = get_cached_url(short_code)
    if cached_url:
        link_id = decode_base62(short_code)
        # Schedule the background task
        background_tasks.add_task(log_click_in_background, link_id, referrer, country)
        return RedirectResponse(url=cached_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    # 2. Slow Path: Check PostgreSQL (Disk)
    db_link = db.query(models.Link).filter(models.Link.short_code == short_code).first()
    if not db_link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short link not found")

    # 3. Populate Redis
    set_cached_url(short_code, db_link.long_url)

    # 4. Schedule the background task
    background_tasks.add_task(log_click_in_background, db_link.id, referrer, country)

    # 5. Return redirect immediately
    return RedirectResponse(url=db_link.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)