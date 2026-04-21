"""
Database configuration and session management.
Supports SQLite (default, zero-setup) and MySQL (for production/demo).

To use SQLite (default):
    DATABASE_URL=sqlite:///./incidents.db

To use MySQL:
    DATABASE_URL=mysql+pymysql://root:password@localhost:3306/incident_management
"""
"""
Database configuration file.
Handles connection to MySQL database using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🔴 CHANGE THESE VALUES
USERNAME = "root"
PASSWORD = "MYSQLROOT"
HOST = "localhost"
DATABASE = "NT_BATCH_6_Incident_Management_System"

DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"

# Create engine
engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """
    Dependency for getting DB session.
    Used by FastAPI routes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()