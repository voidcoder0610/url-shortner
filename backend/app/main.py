from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import shorten, redirect

# 1. Automatically create tables in the database if they don't exist yet
models.Base.metadata.create_all(bind=engine)

# 2. Instantiate the core FastAPI application
app = FastAPI(
    title="URL Shortener API",
    description="A high-speed URL shortener with Redis caching and PostgreSQL storage.",
    version="1.0.0"
)

# 3. Mount our routers
app.include_router(shorten.router)
app.include_router(redirect.router)


@app.get("/")
def health_check():
    """Simple health check endpoint to confirm the server is running."""
    return {"status": "ok", "message": "URL Shortener API is live!"}