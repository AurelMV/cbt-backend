from typing import List
from pydantic import BaseModel, EmailStr


class RoleRead(BaseModel):
    name: str


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    roles: List[RoleRead]

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str
