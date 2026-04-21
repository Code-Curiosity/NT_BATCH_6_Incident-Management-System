"""
Team database model.
Represents different teams handling incidents.
"""

from sqlalchemy import Column, Integer, String

from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }