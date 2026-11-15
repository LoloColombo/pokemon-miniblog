from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

SLUG_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=60)
    slug: str = Field(..., min_length=2, max_length=60, pattern=SLUG_PATTERN)


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=60)
    slug: Optional[str] = Field(None, min_length=2, max_length=60, pattern=SLUG_PATTERN)


class CategoryPublic(BaseModel):
    id: int
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedCategories(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    items: List[CategoryPublic]
