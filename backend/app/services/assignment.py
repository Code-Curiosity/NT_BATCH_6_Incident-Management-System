"""
Incident Assignment Engine.
Assigns incidents to users based on workload (max 3 active incidents).
"""


def assign_user(db, team: str) -> str:
    """
    Assign an incident to a user based on workload.

    Args:
        db: Database session
        team: Team name (DevOps Team / Application Team)

    Returns:
        assigned user name
    """
    from app.models.user import User
    from app.models.incident import Incident

    users = db.query(User).filter(User.team == team).all()

    for user in users:
        active_count = _get_active_incident_count(db, user.name)

        if active_count < 3:
            return user.name

    # fallback if all users overloaded
    return users[0].name if users else None


def _get_active_incident_count(db, username: str) -> int:
    """
    Count active incidents assigned to a user.
    """
    from app.models.incident import Incident

    return db.query(Incident).filter(
        Incident.assigned_user == username,
        Incident.active == True
    ).count()