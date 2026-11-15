from __future__ import annotations
from typing import List, Literal, TYPE_CHECKING
from sqlalchemy import Boolean, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

if TYPE_CHECKING:
    from .post import PostORM

Role = Literal["user", "editor", "admin"]
ROLE_LEVELS = {"user": 0, "editor": 1, "admin": 2}


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(
        Enum("user", "editor", "admin", name="user_role"),
        default="user"
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    posts: Mapped[List["PostORM"]] = relationship(back_populates="user")
