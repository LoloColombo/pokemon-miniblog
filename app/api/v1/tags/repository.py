from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models import TagORM, PostORM, post_tags
from app.services.pagination import paginate_query


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, tag_id: int) -> Optional[TagORM]:
        return self.db.get(TagORM, tag_id)

    def get_by_name(self, name: str) -> Optional[TagORM]:
        query = select(TagORM).where(func.lower(TagORM.name) == name.strip().lower())
        return self.db.execute(query).scalars().first()

    def list_tags(self, search: Optional[str], page: int, per_page: int, order_by: str, direction: str) -> dict:
        query = select(TagORM)
        if search:
            query = query.where(TagORM.name.ilike(f"%{search}%"))

        return paginate_query(
            self.db,
            TagORM,
            base_query=query,
            page=page,
            per_page=per_page,
            order_by=order_by,
            direction=direction,
            allowed_order={"id": TagORM.id, "name": func.lower(TagORM.name)},
        )

    def create_tag(self, name: str) -> TagORM:
        normalized = name.strip().lower()
        existing = self.get_by_name(normalized)
        if existing:
            return existing

        tag = TagORM(name=normalized)
        self.db.add(tag)
        self.db.flush()
        return tag

    def update(self, tag: TagORM, name: str) -> TagORM:
        tag.name = name.strip().lower()
        self.db.flush()
        return tag

    def delete(self, tag_id: int) -> bool:
        tag = self.get(tag_id)
        if not tag:
            return False
        self.db.delete(tag)
        return True

    def most_popular(self) -> Optional[dict]:
        row = self.db.execute(
            select(
                TagORM.id,
                TagORM.name,
                func.count(PostORM.id).label("uses")
            )
            .join(post_tags, post_tags.c.tag_id == TagORM.id)
            .join(PostORM, PostORM.id == post_tags.c.post_id)
            .group_by(TagORM.id, TagORM.name)
            .order_by(func.count(PostORM.id).desc())
            .limit(1)
        ).mappings().first()

        return dict(row) if row else None
