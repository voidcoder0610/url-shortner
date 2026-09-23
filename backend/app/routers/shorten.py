from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from app.utils import encode_base62
from app.cache import set_cached_url

router = APIRouter(tags=["Shorten"])


# Dependency: Opens a database session for this request, and closes it when finished
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/shorten", response_model=schemas.URLResponse)
def create_short_url(
    payload: schemas.URLCreate, 
    request: Request, 
    db: Session = Depends(get_db)
):
    # Step 1: Create a placeholder link in Postgres to get the unique auto-increment ID
    db_link = models.Link(long_url=payload.long_url, short_code="temp")
    db.add(db_link)
    db.commit()
    db.refresh(db_link)

    # Step 2: Convert that unique database ID into our Base62 short code
    short_code = encode_base62(db_link.id)
    db_link.short_code = short_code
    db.commit()
    db.refresh(db_link)

    # Step 3: Pre-warm the Redis cache so the very first click is instant!
    set_cached_url(short_code, db_link.long_url)

    # Step 4: Build the full clickable URL (e.g., http://localhost:8000/r/gb)
    base_url = str(request.base_url)
    full_short_url = f"{base_url}r/{short_code}"

    # Step 5: Return the validated Pydantic response
    return schemas.URLResponse(
        id=db_link.id,
        short_code=db_link.short_code,
        long_url=db_link.long_url,
        short_url=full_short_url,
        created_at=db_link.created_at
    )