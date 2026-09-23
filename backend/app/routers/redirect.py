from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.cache import get_cached_url, set_cached_url

router = APIRouter(tags=["Redirect"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/r/{short_code}")
def redirect_to_long_url(short_code: str, db: Session = Depends(get_db)):
    # 1. Fast Path: Check Redis Cache (RAM)
    cached_url = get_cached_url(short_code)
    if cached_url:
        return RedirectResponse(
            url=cached_url, 
            status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )

    # 2. Slow Path: Check PostgreSQL (Disk)
    db_link = db.query(models.Link).filter(models.Link.short_code == short_code).first()
    if not db_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Short link not found"
        )

    # 3. Populate Redis so future clicks are instant
    set_cached_url(short_code, db_link.long_url)

    # 4. Redirect visitor with 307
    return RedirectResponse(
        url=db_link.long_url, 
        status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )