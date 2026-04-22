from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, JSON
from app.database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    severity = Column(Enum('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', name='incident_severities'), nullable=False)
    incident_type = Column(Enum('INFRASTRUCTURE', 'APPLICATION', 'PLATFORM', 'SECURITY', name='incident_types'), nullable=False)
    status = Column(Enum('OPEN', 'ACKNOWLEDGED', 'ESCALATED', 'IN_PROGRESS', 'RESOLVED', name='incident_statuses'), default='OPEN')
    
    source = Column(String(100))
    assigned_team = Column(Integer, ForeignKey("teams.id"))
    assigned_user = Column(Integer, ForeignKey("users.id"))
    
    priority_score = Column(Integer, default=0)
    sla_deadline = Column(TIMESTAMP)
    ack_deadline = Column(TIMESTAMP, nullable=True)
    escalation_count = Column(Integer, default=0)
    
    affected_services = Column(JSON)
    root_cause = Column(Text)
    resolution_time = Column(Integer)
    
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(TIMESTAMP, nullable=True)

    def _iso(self, dt):
        """Return ISO string with Z suffix so the browser knows it's UTC."""
        return dt.isoformat() + "Z" if dt else None

    def to_dict(self):
        return {
            "id": self.id,
            "alert_id": self.alert_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "incident_type": self.incident_type,
            "status": self.status,
            "source": self.source,
            "assigned_team": self.assigned_team,
            "assigned_user": self.assigned_user,
            "priority_score": self.priority_score,
            "sla_deadline": self._iso(self.sla_deadline),
            "ack_deadline": self._iso(self.ack_deadline),
            "escalation_count": self.escalation_count,
            "affected_services": self.affected_services,
            "created_at": self._iso(self.created_at),
            "updated_at": self._iso(self.updated_at),
            "resolved_at": self._iso(self.resolved_at),
        }
