import random
from sqlalchemy.orm import Session
from app.models.team import Team
from app.models.user import User

def auto_assign_to_team_member(team_id: int, db: Session):
    """
    Pick a random member from the team for assignment.
    """
    members = db.query(User).filter(User.team_id == team_id).all()
    if not members:
        return None
    return random.choice(members)

def get_team_head(team_id: int, db: Session):
    """
    Get the head user of a team.
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team or not team.head_user_id:
        return None
    return db.query(User).filter(User.id == team.head_user_id).first()

def get_team_by_name(team_name: str, db: Session):
    """
    Find a team by name.
    """
    return db.query(Team).filter(Team.name.ilike(f"%{team_name}%")).first()
