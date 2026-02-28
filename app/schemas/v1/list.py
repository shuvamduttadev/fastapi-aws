from pydantic import BaseModel, Field
from typing import Optional, List as PyList
from datetime import datetime


class ListItemBase(BaseModel):
    """Base list item schema"""
    content: str = Field(..., min_length=1, max_length=1000, description="Item content")
    is_completed: bool = Field(default=False, description="Whether item is completed")
    order: int = Field(default=0, ge=0, description="Item order in the list")


class ListItemCreateRequest(ListItemBase):
    """Schema for creating a list item"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "Buy groceries",
                "is_completed": False,
                "order": 0
            }
        }


class ListItemUpdateRequest(BaseModel):
    """Schema for updating a list item"""
    content: Optional[str] = Field(None, min_length=1, max_length=1000, description="Item content")
    is_completed: Optional[bool] = Field(None, description="Whether item is completed")
    order: Optional[int] = Field(None, ge=0, description="Item order in the list")
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_completed": True
            }
        }


class ListItemResponse(ListItemBase):
    """Schema for list item response"""
    id: int = Field(..., description="Item ID")
    list_id: int = Field(..., description="List ID")
    created_at: datetime = Field(..., description="Item creation timestamp")
    updated_at: datetime = Field(..., description="Item last update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "list_id": 1,
                "content": "Buy groceries",
                "is_completed": False,
                "order": 0,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }


class ListBase(BaseModel):
    """Base list schema"""
    title: str = Field(..., min_length=1, max_length=255, description="List title")
    description: Optional[str] = Field(None, max_length=2000, description="List description")
    is_archived: bool = Field(default=False, description="Whether list is archived")


class ListCreateRequest(ListBase):
    """Schema for creating a new list"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Shopping",
                "description": "Weekly shopping list",
                "is_archived": False
            }
        }


class ListUpdateRequest(BaseModel):
    """Schema for updating a list"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="List title")
    description: Optional[str] = Field(None, max_length=2000, description="List description")
    is_archived: Optional[bool] = Field(None, description="Whether list is archived")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Shopping",
                "is_archived": False
            }
        }


class ListResponse(ListBase):
    """Schema for list response without items"""
    id: int = Field(..., description="List ID")
    owner_id: int = Field(..., description="Owner user ID")
    created_at: datetime = Field(..., description="List creation timestamp")
    updated_at: datetime = Field(..., description="List last update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "owner_id": 1,
                "title": "Shopping",
                "description": "Weekly shopping list",
                "is_archived": False,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }


class ListDetailResponse(ListResponse):
    """Schema for list response with items"""
    items: PyList[ListItemResponse] = Field(default_factory=list, description="List items")
    
    class Config:
        from_attributes = True


class ListsListResponse(BaseModel):
    """Schema for paginated lists response"""
    total: int = Field(..., description="Total number of lists")
    skip: int = Field(..., description="Number of items skipped")
    limit: int = Field(..., description="Number of items returned")
    items: PyList[ListResponse] = Field(..., description="List of lists")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 10,
                "skip": 0,
                "limit": 20,
                "items": []
            }
        }
