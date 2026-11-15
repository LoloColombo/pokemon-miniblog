import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from app.core.db import get_db
from app.models import UserORM
from app.models.user import ROLE_LEVELS

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

password_hash = PasswordHash.recommended()

credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No autenticado",
    headers={"WWW-Authenticate": "Bearer"}
)


def raise_expired_token():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )


def raise_forbidden():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos suficientes",
    )


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(
        tz=timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    playload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    return playload


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserORM:
    try:
        playload = decode_token(token)
    except ExpiredSignatureError:
        raise raise_expired_token()
    except InvalidTokenError:
        raise credentials_exc

    sub: Optional[str] = playload.get("sub")
    if not sub or not sub.isdigit():
        raise credentials_exc

    user = db.get(UserORM, int(sub))
    if not user or not user.is_active:
        raise credentials_exc

    return user


def require_role(min_role: str):
    def checker(user: UserORM = Depends(get_current_user)) -> UserORM:
        if ROLE_LEVELS[user.role] < ROLE_LEVELS[min_role]:
            raise raise_forbidden()
        return user

    return checker


require_editor = require_role("editor")
require_admin = require_role("admin")
