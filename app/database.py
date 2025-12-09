# backend/app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read DATABASE_URL from environment (Render or Local system)
# If not found, fallback to local SQLite
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://canteen_user:secretpw@localhost:5432/canteen_db"
)

# Correct engine connection setup
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

# Session creation
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model class
Base = declarative_base()
