from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.team import Team
from app.models.user import User

router = APIRouter()

@router.get("/")
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    return [{"id": t.id, "name": t.name, "team_type": t.team_type} for t in teams]
