from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import require_editor, require_admin
from .repository import CategoryRepository
from .schemas import CategoryCreate, CategoryPublic, CategoryUpdate, PaginatedCategories

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=PaginatedCategories)
def list_categories(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    repository = CategoryRepository(db)
    return repository.list_categories(page, per_page)


@router.get("/slug/{slug}", response_model=CategoryPublic)
def get_category_by_slug(slug: str, db: Session = Depends(get_db)):
    repository = CategoryRepository(db)
    category = repository.get_by_slug(slug)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category


@router.get("/{category_id}", response_model=CategoryPublic)
def get_category(category_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    repository = CategoryRepository(db)
    category = repository.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category


@router.post("", response_model=CategoryPublic, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), user=Depends(require_editor)):
    repository = CategoryRepository(db)
    if repository.get_by_slug(data.slug):
        raise HTTPException(status_code=400, detail="Slug en uso")
    if repository.get_by_name(data.name):
        raise HTTPException(status_code=400, detail="Nombre en uso")

    category = repository.create(name=data.name, slug=data.slug)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryPublic)
def update_category(data: CategoryUpdate, category_id: int = Path(..., ge=1), db: Session = Depends(get_db), user=Depends(require_editor)):
    repository = CategoryRepository(db)
    category = repository.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    updates = data.model_dump(exclude_unset=True, exclude_none=True)
    if "slug" in updates:
        other = repository.get_by_slug(updates["slug"])
        if other and other.id != category.id:
            raise HTTPException(status_code=400, detail="Slug en uso")

    try:
        repository.update(category, updates)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Nombre en uso")

    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int = Path(..., ge=1), db: Session = Depends(get_db), user=Depends(require_admin)):
    repository = CategoryRepository(db)
    category = repository.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    repository.delete(category)
    db.commit()
