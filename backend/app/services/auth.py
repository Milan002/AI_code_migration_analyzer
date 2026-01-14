"""
Authentication service for JWT token handling and password hashing.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId

from ..config import settings
from ..database.mongodb import get_database
from ..models.user import TokenData, UserInDB


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer security scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None:
            return None
        
        return TokenData(user_id=user_id, email=email)
    except JWTError:
        return None


def users_collection():
    """Get the users collection."""
    db = get_database()
    return db["users"]


async def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Get a user by email."""
    user = await users_collection().find_one({"email": email})
    if user:
        user["_id"] = str(user["_id"])
        return UserInDB(**user)
    return None


async def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    """Get a user by ID."""
    try:
        user = await users_collection().find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            return UserInDB(**user)
    except Exception:
        pass
    return None


async def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    """Authenticate a user with email and password."""
    user = await get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserInDB:
    """
    Dependency to get the current authenticated user from JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    token_data = decode_access_token(token)
    
    if token_data is None or token_data.user_id is None:
        raise credentials_exception
    
    user = await get_user_by_id(token_data.user_id)
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[UserInDB]:
    """
    Optional dependency - returns user if authenticated, None otherwise.
    Useful for routes that work both authenticated and unauthenticated.
    """
    if credentials is None:
        return None
    
    token = credentials.credentials
    token_data = decode_access_token(token)
    
    if token_data is None or token_data.user_id is None:
        return None
    
    user = await get_user_by_id(token_data.user_id)
    return user
