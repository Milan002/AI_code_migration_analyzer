"""
User model for authentication.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    username: str


class UserCreate(BaseModel):
    """Model for user registration."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Model for user login."""
    email: EmailStr
    password: str


class UserInDB(UserBase):
    """User model as stored in database."""
    id: Optional[str] = Field(None, alias="_id")
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


class UserResponse(UserBase):
    """User response model (without password)."""
    id: str
    is_active: bool
    created_at: Optional[datetime] = None


class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    user_id: Optional[str] = None
    email: Optional[str] = None
