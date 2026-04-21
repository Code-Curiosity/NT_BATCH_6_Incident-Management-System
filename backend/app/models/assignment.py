from datetime import datetime
from sqlalchemy import Column, Integer, Enum, ForeignKey, TIMESTAMP
from app.database import Base

class IncidentAssignmentQueue(Base):
    __tablename__ = "incident_assignment_queue"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tried_at = Column(TIMESTAMP, default=datetime.utcnow)
    result = Column(Enum('PENDING', 'ACKNOWLEDGED', 'SKIPPED_BUSY', 'SKIPPED_NO_ACK', name='queue_results'), nullable=False)

class UnacknowledgedIncident(Base):
    __tablename__ = "unacknowledged_incidents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False, unique=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    queued_at = Column(TIMESTAMP, default=datetime.utcnow)
    reassigned_at = Column(TIMESTAMP, nullable=True)
    reassigned_to = Column(Integer, nullable=True)
