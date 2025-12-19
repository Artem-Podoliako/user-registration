"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import User
from schemas import RegisterRequest, RegisterResponse
from utils import hash_password
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["auth"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with login and password"
)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    
    - **login**: 3-32 characters, letters/numbers/._-
    - **password**: At least 8 chars with uppercase, lowercase, digit, and special char
    
    Returns 201 on success, 422 on validation error, 409 on duplicate login.
    """
    # Check if user already exists
    result = await db.execute(
        select(User).where(User.login == request.login)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        logger.error(f"Registration failed: duplicate login '{request.login}'")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Login already exists"
        )
    
    # Hash password (never log the password)
    password_hash = hash_password(request.password)
    
    # Create new user
    new_user = User(
        login=request.login,
        password_hash=password_hash
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    logger.info(f"User registered successfully: login='{request.login}'")
    
    return RegisterResponse(message="user создан")

