from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from app.api.v1.auth.schemas import UserPublic
from app.core.db import get_db
from app.core.security import require_admin
from app.models import UserORM
from .repository import UserRepository
from .schemas import ActiveUpdate, PaginatedUsers, RoleUpdate

router = APIRouter(prefix="/users", tags=["users"])


def get_user_or_404(repository: UserRepository, user_id: int) -> UserORM:
    user = repository.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.get("", response_model=PaginatedUsers)
def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    admin: UserORM = Depends(require_admin)
):
    repository = UserRepository(db)
    return repository.list_users(page, per_page)


@router.get("/{user_id}", response_model=UserPublic)
def get_user(user_id: int = Path(..., ge=1), db: Session = Depends(get_db), admin: UserORM = Depends(require_admin)):
    return get_user_or_404(UserRepository(db), user_id)


@router.patch("/{user_id}/role", response_model=UserPublic)
def change_role(data: RoleUpdate, user_id: int = Path(..., ge=1), db: Session = Depends(get_db), admin: UserORM = Depends(require_admin)):
    repository = UserRepository(db)
    user = get_user_or_404(repository, user_id)
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="No podés cambiar tu propio rol")

    repository.set_role(user, data.role)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}/active", response_model=UserPublic)
def change_active(data: ActiveUpdate, user_id: int = Path(..., ge=1), db: Session = Depends(get_db), admin: UserORM = Depends(require_admin)):
    repository = UserRepository(db)
    user = get_user_or_404(repository, user_id)
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="No podés desactivar tu propia cuenta")

    repository.set_active(user, data.is_active)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int = Path(..., ge=1), db: Session = Depends(get_db), admin: UserORM = Depends(require_admin)):
    repository = UserRepository(db)
    user = get_user_or_404(repository, user_id)
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="No podés eliminar tu propia cuenta")

    repository.delete(user)
    db.commit()
