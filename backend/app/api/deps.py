import uuid
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable
from app.database import get_db
from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.models.user import User
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = decode_token(token)
        user_id_raw = payload.get("user_id")
        if user_id_raw is None:
            raise UnauthorizedException(detail="Invalid credentials")
        user_id = uuid.UUID(str(user_id_raw))
    except Exception:
        raise UnauthorizedException(detail="Could not validate credentials")

    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise UnauthorizedException(detail="User not found")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise UnauthorizedException(detail="Inactive user")
    return current_user

def require_role(required_roles: list[str] | str) -> Callable:
    if isinstance(required_roles, str):
        target_roles = [required_roles.upper()]
    else:
        target_roles = [r.upper() for r in required_roles]

    async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if (current_user.role or "").upper() not in target_roles:
            raise ForbiddenException(detail="Not enough permissions")
        return current_user
    return role_checker

require_admin = require_role(["ADMIN"])
require_facilitator = require_role(["ADMIN", "FACILITATOR"])
