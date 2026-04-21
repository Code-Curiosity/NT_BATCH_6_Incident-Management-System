from sqlalchemy.orm import Session
from app.models.team import Team
from app.models.user import User
from app.models.incident import Incident
from app.database import SessionLocal, engine, Base

def seed_data():
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(Team).first():
            print("Database already seeded.")
            return

        print("Seeding database...")

        # 1. Create Teams
        teams_data = [
            {"name": "DevOps Team"},
            {"name": "Auth Service Team"},
            {"name": "Storage Service Team"},
            {"name": "Payment Service Team"},
        ]
        
        teams = []
        for t_data in teams_data:
            team = Team(name=t_data["name"])
            db.add(team)
            teams.append(team)
        
        db.commit()

        # 2. Create Users for each team
        users_config = {
            "DevOps Team": [
                {"name": "Alice DevOps", "email": "alice@company.com"},
                {"name": "Bob DevOps", "email": "bob@company.com"},
                {"name": "Charlie DevOps", "email": "charlie@company.com"},
            ],
            "Auth Service Team": [
                {"name": "Alice Auth", "email": "alice_auth@company.com"},
                {"name": "Bob Auth", "email": "bob_auth@company.com"},
            ],
            "Storage Service Team": [
                {"name": "Alice Storage", "email": "alice_storage@company.com"},
                {"name": "Bob Storage", "email": "bob_storage@company.com"},
            ],
            "Payment Service Team": [
                {"name": "Alice Payment", "email": "alice_payment@company.com"},
                {"name": "Bob Payment", "email": "bob_payment@company.com"},
            ]
        }

        for team in teams:
            team_users = users_config[team.name]
            for i, u_data in enumerate(team_users):
                user = User(name=u_data["name"], email=u_data["email"], team_id=team.id)
                db.add(user)
                db.flush() # To get the user ID
                
                # Set the first user as the head
                if i == 0:
                    team.head_user_id = user.id
            
        db.commit()
        print("Seeding complete!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
