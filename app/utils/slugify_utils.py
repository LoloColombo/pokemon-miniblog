from typing import Optional
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import PostORM


def slugify_base(text: str, max_length: int = 150) -> str:
    base = slugify(text, max_length=max_length, word_boundary=True)
    return base or "post"


def ensure_unique_slug(db: Session, base_text: str, exclude_id: Optional[int] = None) -> str:
    base = slugify_base(base_text)
    query = select(PostORM.slug).where(PostORM.slug.like(f"{base}%"))
    if exclude_id is not None:
        query = query.where(PostORM.id != exclude_id)
    existing = set(db.execute(query).scalars().all())

    if base not in existing:
        return base

    i = 2
    candidate = f"{base}-{i}"
    while candidate in existing:
        i += 1
        candidate = f"{base}-{i}"
    return candidate
