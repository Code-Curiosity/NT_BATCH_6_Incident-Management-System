"""
Incident database model.
Represents an incident in the system with severity, status, and assignment tracking.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean

from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Severity: CRITICAL, HIGH, MEDIUM, LOW
    severity = Column(String(50), nullable=False)

    # Status: NEW, ACKNOWLEDGED, ESCALATED, RESOLVED
    status = Column(String(50), default="NEW")

    # Assignment fields
    assigned_team = Column(String(100), nullable=True)   # DevOps / App Team
    assigned_user = Column(String(100), nullable=True)   # Specific user name

    # ✅ NEW FIELD (for workload logic)
    active = Column(Boolean, default=True)

    # Source: infrastructure / application
    source = Column(String(100), nullable=True)

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
            "assigned_team": self.assigned_team,
            "assigned_user": self.assigned_user,
            "active": self.active,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
