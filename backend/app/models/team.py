from sqlalchemy import Column, Integer, String, Enum
from app.database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    team_type = Column(Enum('INFRASTRUCTURE', 'APPLICATION', 'PLATFORM', 'SECURITY', name='team_types'), nullable=False)