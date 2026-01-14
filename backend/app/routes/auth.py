"""
Authentication routes for user registration and login.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta

from ..models.user import UserCreate, UserLogin, UserResponse, Token, UserInDB
from ..services.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_user_by_email,
    users_collection,
    get_current_user
)
from ..config import settings


router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user.
    
    - **email**: Valid email address (must be unique)
    - **username**: Username (3-50 characters)
    - **password**: Password (minimum 6 characters)
    """
    # Check if email already exists
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user document
    from datetime import datetime
    user_doc = {
        "email": user_data.email,
        "username": user_data.username,
        "hashed_password": get_password_hash(user_data.password),
        "is_active": True,
        "created_at": datetime.utcnow(),
    }
    
    # Insert into database
    result = await users_collection().insert_one(user_doc)
    
    # Return created user
    return UserResponse(
        id=str(result.inserted_id),
        email=user_data.email,
        username=user_data.username,
        is_active=True,
        created_at=user_doc.get("created_at")
    )


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """
    Login and get an access token.
    
    - **email**: Your registered email
    - **password**: Your password
    
    Returns a JWT token to use in the Authorization header.
    """
    user = await authenticate_user(user_data.email, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserInDB = Depends(get_current_user)):
    """
    Get current authenticated user's information.
    
    Requires a valid JWT token in the Authorization header.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )
