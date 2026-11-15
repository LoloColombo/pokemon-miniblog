from math import ceil
from typing import Any, Dict, Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session


def paginate_query(
    db: Session,
    model,
    base_query=None,
    page: int = 1,
    per_page: int = 10,
    order_by: Optional[str] = None,
    direction: str = "asc",
    allowed_order: Optional[Dict[str, Any]] = None,
) -> dict:
    query = base_query if base_query is not None else select(model)

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    total_pages = ceil(total / per_page) if total > 0 else 0
    current_page = 1 if total_pages == 0 else min(max(page, 1), total_pages)

    allowed_order = allowed_order or {"id": model.id}
    order_col = allowed_order.get(order_by or "id", model.id)
    query = query.order_by(
        order_col.desc() if direction == "desc" else order_col.asc())

    items = []
    if total > 0:
        items = db.execute(
            query.offset((current_page - 1) * per_page).limit(per_page)
        ).scalars().all()

    return {
        "page": current_page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_prev": current_page > 1,
        "has_next": current_page < total_pages,
        "items": items,
    }
