from fastapi import APIRouter, Depends, Security
from sqlmodel import Session, select

from api.deps import get_current_user
from db.base import get_session
from db.models.user import User
from schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: User = Security(get_current_user, scopes=["user"]),
    session: Session = Depends(get_session),
):
    return current_user


@router.get("/", response_model=list[UserRead])
async def read_all_users(
    current_user: User = Security(get_current_user, scopes=["admin"]),
    session: Session = Depends(get_session),
):
    users = session.exec(select(User)).all()
    return users
