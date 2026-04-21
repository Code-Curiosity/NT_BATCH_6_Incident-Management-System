from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.user import User

router = APIRouter()

@router.get("/")
def get_users(team_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(User)
    if team_id:
        query = query.filter(User.team_id == team_id)
    users = query.all()
    return [user.to_dict() for user in users]
