# backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# read DATABASE_URL from env, fallback to sqlite for local dev if not present
DATABASE_URL = os.getenv("postgresql://canteen_user:secretpw@localhost:5432/canteen_db", "sqlite:///./canteen.db")

# If using Heroku-style DATABASE_URL with postgres, SQLAlchemy needs no change.
# But if using windows and psycopg2, ensure 'postgresql+psycopg2://' scheme is used.

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
