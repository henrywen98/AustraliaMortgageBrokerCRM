from sqlmodel import Session
from app.db.session import engine
from app.models import User, UserRole, Client, Deal, Task
from app.core.security import hash_password


def run():
    with Session(engine) as db:
        admin = User(email="admin@example.com", hashed_password=hash_password("admin123"), role=UserRole.Admin)
        broker1 = User(email="broker1@example.com", hashed_password=hash_password("broker123"), role=UserRole.Broker)
        broker2 = User(email="broker2@example.com", hashed_password=hash_password("broker123"), role=UserRole.Broker)
        db.add(admin); db.add(broker1); db.add(broker2)
        db.commit()
        db.refresh(broker1)
        c = Client(name="Alice", contact={"phone":"0400***123"})
        db.add(c); db.commit(); db.refresh(c)
        d = Deal(client_id=c.id, owner_user_id=broker1.id, lender="CBA", loan_type="Home Loan", amount=500000)
        db.add(d); db.commit(); db.refresh(d)
        t = Task(deal_id=d.id, title="Collect payslips", assignee_user_id=broker1.id)
        db.add(t); db.commit()
        print("Seed data created.")


if __name__ == "__main__":
    run()

