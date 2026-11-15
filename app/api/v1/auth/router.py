from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import create_access_token, get_current_user
from app.api.v1.users.repository import UserRepository
from app.models import UserORM
from .schemas import Token, UserCreate, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    if repository.get_by_email(data.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    if repository.get_by_username(data.username):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

    user = repository.create(username=data.username, email=data.email, password=data.password)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    repository = UserRepository(db)
    user = repository.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "role": user.role}
    )

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserPublic)
def read_me(current: UserORM = Depends(get_current_user)):
    return current
