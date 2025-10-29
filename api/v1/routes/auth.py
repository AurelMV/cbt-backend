from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from db.base import get_session
from schemas.user import UserCreate, UserRead, Token
from services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_create: UserCreate, session: Session = Depends(get_session)):
    return register_user(session, user_create)


@router.post(
    "/login",
    response_model=Token,
    description="Use the 'username' field to send either your username or your email.",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    return login_user(session, form_data.username, form_data.password)
