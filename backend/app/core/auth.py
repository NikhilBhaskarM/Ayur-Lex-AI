"""
Core Authentication & Role-Based Access Control (RBAC) for Ayur-Lex-AI.

Provides:
- JWT token generation & validation with JWT_SECRET_KEY
- Seeded accounts: 'admin' (AdminAyur@2026) and 'ayur_user' (UserAyur@2026)
- get_current_user dependency validating Bearer tokens with graceful local fallback
- require_role([roles]) dependency guard raising HTTPException(403, "Insufficient permissions")
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

# Secret configuration with safe local development fallback
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ayur_lex_ai_jwt_secret_key_2026_secure")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 hours

import bcrypt

# Seeded user accounts in memory (with backward-compatibility aliases)
SEEDED_USERS: Dict[str, Dict[str, Any]] = {
    "admin": {
        "username": "admin",
        "password": "AdminAyur@2026",
        "role": "admin",
        "email": "admin@ayurlex.ai",
        "full_name": "System Administrator",
    },
    "ayur_user": {
        "username": "ayur_user",
        "password": "UserAyur@2026",
        "role": "user",
        "email": "user@ayurlex.ai",
        "full_name": "Ayur-Lex User",
    },
    # Backwards-compatible aliases for existing developer sessions
    "admin@ayurlex.ai": {
        "username": "admin",
        "password": "Admin@123",
        "role": "admin",
        "email": "admin@ayurlex.ai",
        "full_name": "System Administrator",
    },
    "researcher@ayurlex.ai": {
        "username": "researcher",
        "password": "Admin@123",
        "role": "admin",
        "email": "researcher@ayurlex.ai",
        "full_name": "Ayur-Lex Researcher",
    },
}


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password."""
    try:
        pwd_bytes = plain_password.encode("utf-8")[:72]
        return bcrypt.checkpw(pwd_bytes, hashed_password.encode("utf-8"))
    except Exception:
        return False


# Pre-compute bcrypt hashes for seeded accounts for fast/secure validation
for u in SEEDED_USERS.values():
    if "password_hash" not in u:
        try:
            u["password_hash"] = hash_password(u["password"])
        except Exception:
            pass


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate username or email against seeded accounts."""
    if not username or not password:
        return None

    # Check direct match by username
    user = SEEDED_USERS.get(username)
    if not user:
        # Check by email lookup
        for account in SEEDED_USERS.values():
            if account.get("email", "").lower() == username.lower():
                user = account
                break

    if not user:
        return None

    # Check password (either exact seeded match or bcrypt hash)
    if user.get("password") == password:
        return user
    if "password_hash" in user and verify_password(password, user["password_hash"]):
        return user

    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Bearer token extractor (optional so endpoints can handle graceful local fallbacks)
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    request: Request = None,
) -> Dict[str, Any]:
    """
    FastAPI dependency validating the Bearer token.
    Supports:
    1. Standard JWT Bearer token via Authorization header
    2. Local development fallback 'demo-access-token'
    3. Custom query/header fallbacks
    """
    token = None
    if credentials:
        token = credentials.credentials
    elif request:
        auth_header = request.headers.get("Authorization") or request.headers.get("authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()

    if not token:
        # Check if environment allows unauthenticated dev fallback
        allow_dev = os.getenv("ALLOW_DEV_ANONYMOUS", "false").lower() == "true"
        if allow_dev:
            return {
                "username": "dev_guest",
                "role": "user",
                "email": "dev@ayurlex.ai",
                "full_name": "Development Guest",
            }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Developer demo access token convenience
    if token == "demo-access-token":
        return {
            "username": "admin",
            "role": "admin",
            "email": "admin@ayurlex.ai",
            "full_name": "Ayur-Lex Administrator",
        }

    payload = decode_token(token)
    username = payload.get("sub") or payload.get("username")
    role = payload.get("role") or "user"

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Normalize role to lowercase ('admin' or 'user')
    role = str(role).lower()

    # Look up user or construct from claims
    user_info = SEEDED_USERS.get(username)
    if user_info:
        return {
            "username": user_info.get("username", username),
            "role": user_info.get("role", role).lower(),
            "email": user_info.get("email"),
            "full_name": user_info.get("full_name"),
        }

    return {
        "username": username,
        "role": role,
        "email": payload.get("email", f"{username}@ayurlex.ai"),
        "full_name": payload.get("full_name", username),
    }


def require_role(allowed_roles: List[str]):
    """
    Role guard dependency.
    If user role is not in allowed_roles, raises HTTPException(403, "Insufficient permissions").
    """
    normalized_allowed = [r.strip().lower() for r in allowed_roles]

    async def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        user_role = str(current_user.get("role", "")).strip().lower()
        if user_role not in normalized_allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return role_checker
