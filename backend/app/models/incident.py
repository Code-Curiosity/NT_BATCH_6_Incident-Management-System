"""
Incident database model.
Represents an incident in the system with severity, status, and assignment tracking.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(50), nullable=False)       # critical, high, medium, low
    status = Column(String(50), default="new")           # new, acknowledged, escalated, resolved
    assigned_to = Column(String(100), nullable=True)     # team or person
    source = Column(String(100), nullable=True)          # infrastructure, application
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
