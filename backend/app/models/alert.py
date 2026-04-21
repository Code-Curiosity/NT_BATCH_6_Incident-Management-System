"""
Alert database model.
Represents incoming alerts from systems.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    message = Column(Text, nullable=False)
    source = Column(String(100), nullable=True)   # logs, monitoring tool

    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }