"""
Database configuration and session management.
Supports SQLite (default, zero-setup) and MySQL (for production/demo).

To use SQLite (default):
    DATABASE_URL=sqlite:///./incidents.db

To use MySQL:
    DATABASE_URL=mysql+pymysql://root:password@localhost:3306/incident_management
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Database connection URL - defaults to SQLite for easy local development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./incidents.db"
)

# SQLite needs connect_args for thread safety
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
