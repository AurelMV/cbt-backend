from __future__ import annotations
from typing import Optional

from sqlmodel import Session, select
from db.models.user import User, Role, UserRole


def get_by_username(session: Session, username: str) -> Optional[User]:
    return session.exec(select(User).where(User.username == username)).first()


def get_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()


def create(session: Session, user: User) -> User:
    session.add(user)
    session.flush()  # assign PK without committing
    return user


def add_role(session: Session, user: User, role: Role) -> None:
    link = session.exec(
        select(UserRole).where(
            (UserRole.user_id == user.id) & (UserRole.role_id == role.id)
        )
    ).first()
    if not link:
        session.add(UserRole(user_id=user.id, role_id=role.id))
