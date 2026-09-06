import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from app.config import settings
from app.core.exceptions import UnauthorizedException

ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        pwd_bytes = plain_password.encode("utf-8")[:72]
        return bcrypt.checkpw(pwd_bytes, hashed_password.encode("utf-8"))
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        minutes = getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 30)
        expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    to_encode.update({"exp": expire})
    secret_key = getattr(settings, "SECRET_KEY", "fallback_secret")
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    days = getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", 7)
    expire = datetime.now(timezone.utc) + timedelta(days=days)
    to_encode.update({"exp": expire})
    secret_key = getattr(settings, "SECRET_KEY", "fallback_secret")
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        secret_key = getattr(settings, "SECRET_KEY", "fallback_secret")
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise UnauthorizedException(detail="Could not validate credentials")
