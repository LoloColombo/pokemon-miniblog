from typing import List, Literal
from pydantic import BaseModel
from app.api.v1.auth.schemas import UserPublic


class RoleUpdate(BaseModel):
    role: Literal["user", "editor", "admin"]


class ActiveUpdate(BaseModel):
    is_active: bool


class PaginatedUsers(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    items: List[UserPublic]
