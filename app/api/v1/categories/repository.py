from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models import CategoryORM
from app.services.pagination import paginate_query


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, category_id: int) -> Optional[CategoryORM]:
        return self.db.get(CategoryORM, category_id)

    def get_by_slug(self, slug: str) -> Optional[CategoryORM]:
        query = select(CategoryORM).where(CategoryORM.slug == slug)
        return self.db.execute(query).scalars().first()

    def get_by_name(self, name: str) -> Optional[CategoryORM]:
        query = select(CategoryORM).where(func.lower(CategoryORM.name) == name.strip().lower())
        return self.db.execute(query).scalars().first()

    def list_categories(self, page: int, per_page: int) -> dict:
        return paginate_query(
            self.db,
            CategoryORM,
            page=page,
            per_page=per_page,
            order_by="name",
            allowed_order={"id": CategoryORM.id, "name": func.lower(CategoryORM.name)},
        )

    def create(self, *, name: str, slug: str) -> CategoryORM:
        category = CategoryORM(name=name.strip(), slug=slug)
        self.db.add(category)
        self.db.flush()
        return category

    def update(self, category: CategoryORM, updates: dict) -> CategoryORM:
        for key, value in updates.items():
            setattr(category, key, value)
        self.db.flush()
        return category

    def delete(self, category: CategoryORM) -> None:
        self.db.delete(category)
