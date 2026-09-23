import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# We get the database URL from environment variables, or default to a local Postgres instance
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:0610@localhost:5432/urlshortener"
)

# Engine: the actual connection pool to PostgreSQL
engine = create_engine(DATABASE_URL)

# SessionLocal: creates temporary database sessions for handling requests
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: the parent class all our models will inherit from
Base = declarative_base()