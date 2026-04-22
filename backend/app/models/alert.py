from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message = Column(Text, nullable=False)
    source = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)