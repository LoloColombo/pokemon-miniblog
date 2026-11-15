from contextlib import contextmanager
from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.core.db import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models import CategoryORM, PostORM, TagORM, UserORM
from app.utils.slugify_utils import slugify_base
from .data import CATEGORIES, POSTS, SEED_PASSWORD, TAGS, USERS


@contextmanager
def atomic(db: Session):
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise


def _user_by_email(db: Session, email: str) -> Optional[UserORM]:
    return db.execute(select(UserORM).where(UserORM.email == email)).scalars().first()


def _user_by_username(db: Session, username: str) -> Optional[UserORM]:
    return db.execute(select(UserORM).where(UserORM.username == username)).scalars().first()


def _category_by_slug(db: Session, slug: str) -> Optional[CategoryORM]:
    return db.execute(select(CategoryORM).where(CategoryORM.slug == slug)).scalars().first()


def _tag_by_name(db: Session, name: str) -> Optional[TagORM]:
    return db.execute(select(TagORM).where(func.lower(TagORM.name) == name.lower())).scalars().first()


def _post_by_slug(db: Session, slug: str) -> Optional[PostORM]:
    return db.execute(select(PostORM).where(PostORM.slug == slug)).scalars().first()


def seed_users(db: Session) -> None:
    with atomic(db):
        for data in USERS:
            obj = _user_by_email(db, data["email"])
            if obj:
                obj.username = data["username"]
                obj.role = data["role"]
                obj.is_active = True
            else:
                db.add(UserORM(
                    username=data["username"],
                    email=data["email"],
                    role=data["role"],
                    is_active=True,
                    hashed_password=hash_password(SEED_PASSWORD),
                ))


def seed_categories(db: Session) -> None:
    with atomic(db):
        for data in CATEGORIES:
            obj = _category_by_slug(db, data["slug"])
            if obj:
                obj.name = data["name"]
            else:
                db.add(CategoryORM(**data))


def seed_tags(db: Session) -> None:
    with atomic(db):
        for name in TAGS:
            if not _tag_by_name(db, name):
                db.add(TagORM(name=name))


def seed_posts(db: Session) -> None:
    with atomic(db):
        for data in POSTS:
            slug = slugify_base(data["title"])
            tags = []
            for name in data["tags"]:
                tag = _tag_by_name(db, name)
                if not tag:
                    tag = TagORM(name=name)
                    db.add(tag)
                    db.flush()
                tags.append(tag)

            category = _category_by_slug(db, data["category"])
            user = _user_by_username(db, data["author"])

            obj = _post_by_slug(db, slug)
            if not obj:
                obj = PostORM(slug=slug)
                db.add(obj)

            obj.title = data["title"]
            obj.content = data["content"]
            obj.category = category
            obj.user = user
            obj.tags = tags


def _with_session(*seeders) -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for seeder in seeders:
            seeder(db)
    finally:
        db.close()


def run_users() -> None:
    _with_session(seed_users)


def run_categories() -> None:
    _with_session(seed_categories)


def run_tags() -> None:
    _with_session(seed_tags)


def run_posts() -> None:
    _with_session(seed_users, seed_categories, seed_tags, seed_posts)


def run_all() -> None:
    _with_session(seed_users, seed_categories, seed_tags, seed_posts)
