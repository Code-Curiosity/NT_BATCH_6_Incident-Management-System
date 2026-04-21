"""
User database model.
Represents users handling incidents.
"""

from sqlalchemy import Column, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String(100), nullable=False)
    team = Column(String(100), nullable=True)   # DevOps / App Team

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "team": self.team,
        }