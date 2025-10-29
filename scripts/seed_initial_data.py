import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlmodel import select, Session
from db.base import engine
from db.models.user import User, Role, UserRole
from core.security import hash_password


def seed_user_and_admin():
    # Open a database session directly
    with Session(engine) as session:
        # Check if admin user already exists
        admin_role = session.exec(select(Role).where(Role.name == "admin")).first()
        user_role = session.exec(select(Role).where(Role.name == "user")).first()
        if not admin_role and not user_role:
            print("Roles not found. Please run migrations first.")
            return

        # Verify if admin user exists
        admin_exists = session.exec(
            select(User).where(User.username == "admin")
        ).first()
        if not admin_exists:
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=hash_password("123456"),
            )
            session.add(admin_user)
            session.commit()
            session.refresh(admin_user)
            link = UserRole(user_id=admin_user.id, role_id=admin_role.id)
            session.add(link)
            session.commit()
            link2 = UserRole(user_id=admin_user.id, role_id=user_role.id)
            session.add(link2)
            session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

        # Verify if default user exists
        user_exists = session.exec(select(User).where(User.username == "user")).first()
        if not user_exists:
            default_user = User(
                username="user",
                email="user@example.com",
                hashed_password=hash_password("123456"),
            )
            session.add(default_user)
            session.commit()
            session.refresh(default_user)
            link = UserRole(user_id=default_user.id, role_id=user_role.id)
            session.add(link)
            session.commit()
            print("Default user created.")
        else:
            print("Default user already exists.")


if __name__ == "__main__":
    seed_user_and_admin()
