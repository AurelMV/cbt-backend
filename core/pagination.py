from __future__ import annotations

from typing import Sequence, Optional, Iterable
from sqlmodel import Session, select
from sqlalchemy import or_, func
import math


def build_search_condition(model, columns: Sequence[str], q: Optional[str]):
    if not q:
        return None
    like = f"%{q}%"
    conds = []
    for col in columns:
        attr = getattr(model, col, None)
        if attr is not None:
            conds.append(attr.ilike(like))
    if not conds:
        return None
    return or_(*conds)


def paginate(
    session: Session,
    model,
    *,
    q: Optional[str],
    columns: Sequence[str],
    offset: int,
    limit: int,
):
    """Generic pagination with optional LIKE search across given columns.

    Returns dict with items, total, pages, limit, offset, page.
    """
    offset = max(0, offset)
    limit = max(1, limit)

    like_condition = build_search_condition(model, columns, q)
    base_query = select(model)
    count_query = select(func.count(model.id))  # assumes 'id' PK exists

    if like_condition is not None:
        base_query = base_query.where(like_condition)
        count_query = count_query.where(like_condition)

    items = session.exec(base_query.offset(offset).limit(limit)).all()
    total = session.exec(count_query).one()
    pages = math.ceil(total / limit) if total else 0
    page = offset // limit if limit else 0
    return {
        "items": items,
        "total": total,
        "pages": pages,
        "limit": limit,
        "offset": offset,
        "page": page,
    }
