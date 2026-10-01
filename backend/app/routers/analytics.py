from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal
from app import models, schemas

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{short_code}", response_model=schemas.ClickAnalytics)
def get_link_analytics(short_code: str, db: Session = Depends(get_db)):
    # 1. Verify that the link exists
    db_link = db.query(models.Link).filter(models.Link.short_code == short_code).first()
    if not db_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Short link not found"
        )

    # 2. Count total clicks for this link
    total_clicks = db.query(func.count(models.Click.id)).filter(
        models.Click.link_id == db_link.id
    ).scalar() or 0

    # 3. Group clicks by Referrer (e.g., twitter.com, google.com)
    referrer_rows = db.query(
        models.Click.referrer, 
        func.count(models.Click.id)
    ).filter(
        models.Click.link_id == db_link.id
    ).group_by(models.Click.referrer).all()

    referrers = {
        (ref or "Direct / None"): count for ref, count in referrer_rows
    }

    # 4. Group clicks by Country
    country_rows = db.query(
        models.Click.country, 
        func.count(models.Click.id)
    ).filter(
        models.Click.link_id == db_link.id
    ).group_by(models.Click.country).all()

    countries = {
        (country or "Unknown"): count for country, count in country_rows
    }

    return schemas.ClickAnalytics(
        short_code=db_link.short_code,
        long_url=db_link.long_url,
        total_clicks=total_clicks,
        referrers=referrers,
        countries=countries
    )