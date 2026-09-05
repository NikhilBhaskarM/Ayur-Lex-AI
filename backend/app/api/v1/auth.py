from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.schemas.auth import UserCreate, UserLogin, UserResponse, TokenResponse
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.core.exceptions import UnauthorizedException, ValidationException
from app.api.deps import get_current_active_user
import uuid

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    if len(user_in.password) < 8:
        raise ValidationException(detail="Password must be at least 8 characters long")
        
    result = await db.execute(select(User).filter(User.email == user_in.email))
    if result.scalars().first():
        raise ValidationException(detail="Email already registered")
        
    new_user = User(
        id=uuid.uuid4(),
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        full_name=user_in.full_name,
        role="USER",
        preferred_language="en",
        is_active=True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user_in.email))
    user = result.scalars().first()
    
    if not user or not verify_password(user_in.password, user.password_hash):
        raise UnauthorizedException(detail="Incorrect email or password")
        
    if not user.is_active:
        raise UnauthorizedException(detail="Inactive user")
        
    token_data = {"user_id": str(user.id), "role": user.role}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token():
    # Placeholder for refresh logic
    return TokenResponse(access_token="placeholder", refresh_token="placeholder")

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user
