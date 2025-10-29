from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr


class UserRole(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    role_id: Optional[int] = Field(
        default=None, foreign_key="role.id", primary_key=True
    )


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    users: List["User"] = Relationship(back_populates="roles", link_model=UserRole)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str
    roles: List[Role] = Relationship(back_populates="users", link_model=UserRole)
