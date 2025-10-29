from __future__ import annotations
from typing import Optional

from sqlmodel import Session, select
from db.models.user import Role


def get_by_name(session: Session, name: str) -> Optional[Role]:
    return session.exec(select(Role).where(Role.name == name)).first()
