from typing import Optional
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.models import UserORM
from app.services.pagination import paginate_query


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int) -> Optional[UserORM]:
        return self.db.get(UserORM, user_id)

    def get_by_email(self, email: str) -> Optional[UserORM]:
        query = select(UserORM).where(func.lower(UserORM.email) == email.strip().lower())
        return self.db.execute(query).scalars().first()

    def get_by_username(self, username: str) -> Optional[UserORM]:
        query = select(UserORM).where(func.lower(UserORM.username) == username.strip().lower())
        return self.db.execute(query).scalars().first()

    def get_by_login(self, login: str) -> Optional[UserORM]:
        value = login.strip().lower()
        query = select(UserORM).where(
            or_(func.lower(UserORM.email) == value, func.lower(UserORM.username) == value)
        )
        return self.db.execute(query).scalars().first()

    def authenticate(self, login: str, password: str) -> Optional[UserORM]:
        user = self.get_by_login(login)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create(self, *, username: str, email: str, password: str, role: str = "user") -> UserORM:
        user = UserORM(
            username=username.strip(),
            email=email.strip().lower(),
            hashed_password=hash_password(password),
            role=role,
            is_active=True,
        )
        self.db.add(user)
        self.db.flush()
        return user

    def list_users(self, page: int, per_page: int) -> dict:
        return paginate_query(self.db, UserORM, page=page, per_page=per_page)

    def set_role(self, user: UserORM, role: str) -> UserORM:
        user.role = role
        self.db.flush()
        return user

    def set_active(self, user: UserORM, is_active: bool) -> UserORM:
        user.is_active = is_active
        self.db.flush()
        return user

    def delete(self, user: UserORM) -> None:
        self.db.delete(user)
