"""
Incident Log database model.
Tracks actions performed on incidents.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class IncidentLog(Base):
    __tablename__ = "incident_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    incident_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False)     # acknowledged, resolved
    performed_by = Column(String(100), nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "incident_id": self.incident_id,
            "action": self.action,
            "performed_by": self.performed_by,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }