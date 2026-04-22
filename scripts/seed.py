import os
import sys

# Add the backend directory to Python path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal, engine, Base
from app.models import Team, User

def seed_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()

    teams = [
        Team(id=1, name='Infrastructure Team', email='infra-team@company.com', team_type='INFRASTRUCTURE'),
        Team(id=2, name='Application Team', email='app-team@company.com', team_type='APPLICATION'),
        Team(id=3, name='Platform Team', email='platform-team@company.com', team_type='PLATFORM'),
        Team(id=4, name='Security Team', email='security-team@company.com', team_type='SECURITY')
    ]
    
    for t in teams:
        db.merge(t)
    
    users = [
        User(id=1, name='Alice Chen', email='alice.chen@company.com', team_id=1, role='lead'),
        User(id=2, name='Bob Kumar', email='bob.kumar@company.com', team_id=1, role='engineer'),
        User(id=3, name='Carol White', email='carol.white@company.com', team_id=1, role='engineer'),
        User(id=4, name='David Park', email='david.park@company.com', team_id=1, role='engineer'),
        User(id=5, name='Eva Singh', email='eva.singh@company.com', team_id=1, role='on-call'),
        User(id=6, name='Frank Liu', email='frank.liu@company.com', team_id=2, role='lead'),
        User(id=7, name='Grace Patel', email='grace.patel@company.com', team_id=2, role='engineer'),
        User(id=8, name='Henry Okafor', email='henry.okafor@company.com', team_id=2, role='engineer'),
        User(id=9, name='Iris Nakamura', email='iris.nakamura@company.com', team_id=2, role='engineer'),
        User(id=10, name='James Ramos', email='james.ramos@company.com', team_id=2, role='on-call'),
        User(id=11, name='Karen Johansson', email='karen.johansson@company.com', team_id=3, role='lead'),
        User(id=12, name='Leo Torres', email='leo.torres@company.com', team_id=3, role='engineer'),
        User(id=13, name='Maya Williams', email='maya.williams@company.com', team_id=3, role='engineer'),
        User(id=14, name='Nate Zhao', email='nate.zhao@company.com', team_id=3, role='engineer'),
        User(id=15, name='Olivia Das', email='olivia.das@company.com', team_id=3, role='on-call'),
        User(id=16, name='Paul Nguyen', email='paul.nguyen@company.com', team_id=4, role='lead'),
        User(id=17, name='Quinn Baker', email='quinn.baker@company.com', team_id=4, role='engineer'),
        User(id=18, name='Rosa Martinez', email='rosa.martinez@company.com', team_id=4, role='engineer'),
        User(id=19, name='Sam Ivanov', email='sam.ivanov@company.com', team_id=4, role='engineer'),
        User(id=20, name='Tara Osei', email='tara.osei@company.com', team_id=4, role='on-call')
    ]
    
    for u in users:
        db.merge(u)
        
    db.commit()
    db.close()
    print("Database seeded with 4 teams and 20 users.")

if __name__ == "__main__":
    seed_database()
