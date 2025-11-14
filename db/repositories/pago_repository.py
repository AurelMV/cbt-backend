from typing import List, Optional
from sqlmodel import Session, select
from core.pagination import paginate

from db.models.enrollment import Pago


def list_all(session: Session) -> List[Pago]:
    return session.exec(select(Pago)).all()


def list_paginated(session: Session, q: Optional[str], offset: int, limit: int):
    return paginate(
        session,
        Pago,
        q=q,
        columns=["nroVoucher", "medioPago"],
        offset=offset,
        limit=limit,
    )


def create(session: Session, pago: Pago) -> Pago:
    session.add(pago)
    session.commit()
    session.refresh(pago)
    return pago


def get(session: Session, pago_id: int) -> Optional[Pago]:
    return session.get(Pago, pago_id)
