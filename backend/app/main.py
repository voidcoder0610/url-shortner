from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models
from app.routers import shorten, redirect, analytics

# Automatically create tables in the database if they don't exist yet
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="A high-speed URL shortener with Redis caching and PostgreSQL storage.",
    version="1.0.0"
)

# Configure CORS: Allow our React frontend to make requests to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows all headers
)

# Mount our routers
app.include_router(shorten.router)
app.include_router(redirect.router)
app.include_router(analytics.router)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "URL Shortener API is live!"}