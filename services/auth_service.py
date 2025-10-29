from __future__ import annotations
from typing import Dict

from fastapi import HTTPException, status
from sqlmodel import Session

from core.security import hash_password, verify_password, create_access_token
from schemas.user import UserCreate
from db.models.user import User
from db.repositories import user_repository as users_repo
from db.repositories import role_repository as roles_repo


def register_user(session: Session, data: UserCreate) -> User:
    # Check uniqueness
    if users_repo.get_by_username(session, data.username) or users_repo.get_by_email(
        session, data.email
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    # Create user entity
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    users_repo.create(session, user)

    # Require default role 'user' to exist
    default_role = roles_repo.get_by_name(session, "user")
    if not default_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default role 'user' not found. Seed initial data before registering users.",
        )

    users_repo.add_role(session, user, default_role)
    session.commit()
    session.refresh(user)
    return user


def login_user(session: Session, identifier: str, password: str) -> Dict[str, str]:
    """Login with either username or email plus password.

    The OAuth2 password flow sends the field as 'username' per spec; we interpret
    that field as either the actual username or the email.
    """
    user = users_repo.get_by_username(session, identifier) or users_repo.get_by_email(
        session, identifier
    )
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    roles = [role.name for role in user.roles]
    access_token = create_access_token(data={"sub": user.username, "roles": roles})
    return {"access_token": access_token, "token_type": "bearer"}
