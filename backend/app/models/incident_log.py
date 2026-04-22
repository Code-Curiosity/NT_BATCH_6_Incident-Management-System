from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from app.database import Base

class IncidentLog(Base):
    __tablename__ = "incident_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    action = Column(String(100), nullable=False)
    performed_by = Column(Integer, ForeignKey("users.id"))
    details = Column(Text)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)