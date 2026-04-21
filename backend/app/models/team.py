from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    head_user_id = Column(Integer, ForeignKey("users.id", name="fk_team_head_user"), nullable=True)

    # Relationships
    members = relationship("User", back_populates="team", foreign_keys="User.team_id")
    head_user = relationship("User", foreign_keys=[head_user_id], remote_side="User.id")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "head_user_id": self.head_user_id,
            "head_name": self.head_user.name if self.head_user else None
        }
