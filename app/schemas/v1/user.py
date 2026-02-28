from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List as PyList
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(..., min_length=1, max_length=255, description="User full name")
    is_active: bool = Field(default=True, description="Whether user account is active")


class UserCreateRequest(UserBase):
    """Schema for creating a new user"""
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "is_active": True
            }
        }


class UserUpdateRequest(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = Field(None, description="User email address")
    full_name: Optional[str] = Field(None, min_length=1, max_length=255, description="User full name")
    is_active: Optional[bool] = Field(None, description="Whether user account is active")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "newemail@example.com",
                "full_name": "Jane Doe"
            }
        }


class UserResponse(UserBase):
    """Schema for user response"""
    id: int = Field(..., description="User ID")
    is_superuser: bool = Field(..., description="Whether user is a superuser")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="User last update timestamp")
    last_login: Optional[datetime] = Field(None, description="User last login timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "last_login": None
            }
        }


class PaginationParams(BaseModel):
    """Schema for pagination parameters"""
    skip: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(20, ge=1, le=100, description="Number of items to return")


class UsersListResponse(BaseModel):
    """Schema for paginated users list response"""
    total: int = Field(..., description="Total number of users")
    skip: int = Field(..., description="Number of items skipped")
    limit: int = Field(..., description="Number of items returned")
    items: PyList[UserResponse] = Field(..., description="List of users")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 100,
                "skip": 0,
                "limit": 20,
                "items": []
            }
        }
