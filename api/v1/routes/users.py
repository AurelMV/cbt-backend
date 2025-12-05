from fastapi import APIRouter, Depends, Security
from sqlmodel import Session, select

from api.deps import get_current_user
from db.base import get_session
from db.models.user import User
from schemas.user import UserRead, UserUpdate
from services.auth_service import update_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: User = Security(get_current_user, scopes=["user"]),
    session: Session = Depends(get_session),
):
    return current_user


@router.put("/me", response_model=UserRead)
async def update_users_me(
    user_update: UserUpdate,
    current_user: User = Security(get_current_user, scopes=["user"]),
    session: Session = Depends(get_session),
):
    return update_user(session, current_user, user_update)


@router.get("/", response_model=list[UserRead])
async def read_all_users(
    current_user: User = Security(get_current_user, scopes=["admin"]),
    session: Session = Depends(get_session),
):
    users = session.exec(select(User)).all()
    return users
