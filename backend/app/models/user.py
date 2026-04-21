from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id", name="fk_user_team"), nullable=True)

    # Relationships
    team = relationship("Team", back_populates="members", foreign_keys=[team_id])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "team_id": self.team_id,
            "team_name": self.team.name if self.team else None
        }
