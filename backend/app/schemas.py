from datetime import datetime
from pydantic import BaseModel, HttpUrl


# Schema for the incoming request to shorten a link
class URLCreate(BaseModel):
    long_url: str


# Schema for the outgoing response after a link is created
class URLResponse(BaseModel):
    id: int
    short_code: str
    long_url: str
    short_url: str
    created_at: datetime

    # Enables Pydantic to read data directly from SQLAlchemy database objects
    class Config:
        from_attributes = True