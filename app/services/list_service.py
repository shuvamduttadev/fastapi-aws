from sqlalchemy.orm import Session
from app.repositories.list_repository import ListRepository, ListItemRepository
from app.schemas.v1.list import (
    ListCreateRequest, ListUpdateRequest, ListResponse, ListDetailResponse,
    ListItemCreateRequest, ListItemUpdateRequest, ListItemResponse
)
from fastapi import HTTPException, status
from typing import Optional


class ListService:
    """Service for list business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = ListRepository(db)
        self.item_repository = ListItemRepository(db)
    
    def create_list(self, owner_id: int, list_data: ListCreateRequest) -> ListResponse:
        """Create a new list"""
        db_list = self.repository.create(
            title=list_data.title,
            owner_id=owner_id,
            description=list_data.description
        )
        return ListResponse.from_orm(db_list)
    
    def get_list(self, list_id: int, owner_id: Optional[int] = None) -> ListDetailResponse:
        """Get list with its items"""
        if owner_id:
            db_list = self.repository.get_by_id_and_owner(list_id, owner_id)
        else:
            db_list = self.repository.get_by_id(list_id)
        
        if not db_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found"
            )
        
        return ListDetailResponse.from_orm(db_list)
    
    def get_user_lists(self, owner_id: int, skip: int = 0, limit: int = 20):
        """Get all lists for a user"""
        lists, total = self.repository.get_by_owner(owner_id, skip=skip, limit=limit)
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "items": [ListResponse.from_orm(lst) for lst in lists]
        }
    
    def update_list(self, list_id: int, owner_id: int, list_data: ListUpdateRequest) -> ListResponse:
        """Update list information"""
        db_list = self.repository.get_by_id_and_owner(list_id, owner_id)
        if not db_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found"
            )
        
        update_data = list_data.model_dump(exclude_unset=True)
        updated_list = self.repository.update(list_id, **update_data)
        
        return ListResponse.from_orm(updated_list)
    
    def delete_list(self, list_id: int, owner_id: int) -> None:
        """Delete a list"""
        db_list = self.repository.get_by_id_and_owner(list_id, owner_id)
        if not db_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found"
            )
        
        self.repository.delete(list_id)
    
    def archive_list(self, list_id: int, owner_id: int) -> ListResponse:
        """Archive a list"""
        db_list = self.repository.get_by_id_and_owner(list_id, owner_id)
        if not db_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found"
            )
        
        archived_list = self.repository.archive(list_id)
        return ListResponse.from_orm(archived_list)
    
    def unarchive_list(self, list_id: int, owner_id: int) -> ListResponse:
        """Unarchive a list"""
        db_list = self.repository.get_by_id_and_owner(list_id, owner_id)
        if not db_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found"
            )
        
        unarchived_list = self.repository.unarchive(list_id)
        return ListResponse.from_orm(unarchived_list)


class ListItemService:
    """Service for list item business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = ListItemRepository(db)
        self.list_repository = ListRepository(db)
    
    def create_item(self, list_id: int, owner_id: int, item_data: ListItemCreateRequest) -> ListItemResponse:
        """Create a new list item"""
        # Verify list ownership
        db_list = self.list_repository.get_by_id_and_owner(list_id, owner_id)
        if not db_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found"
            )
        
        item = self.repository.create(
            list_id=list_id,
            content=item_data.content,
            order=item_data.order
        )
        return ListItemResponse.from_orm(item)
    
    def get_item(self, item_id: int, owner_id: int) -> ListItemResponse:
        """Get list item with ownership check"""
        item = self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        # Verify ownership through list
        db_list = self.list_repository.get_by_id_and_owner(item.list_id, owner_id)
        if not db_list:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return ListItemResponse.from_orm(item)
    
    def get_list_items(self, list_id: int, owner_id: int) -> list[ListItemResponse]:
        """Get all items in a list with ownership check"""
        db_list = self.list_repository.get_by_id_and_owner(list_id, owner_id)
        if not db_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found"
            )
        
        items = self.repository.get_by_list(list_id)
        return [ListItemResponse.from_orm(item) for item in items]
    
    def update_item(self, item_id: int, owner_id: int, item_data: ListItemUpdateRequest) -> ListItemResponse:
        """Update list item"""
        item = self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        # Verify ownership through list
        db_list = self.list_repository.get_by_id_and_owner(item.list_id, owner_id)
        if not db_list:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        update_data = item_data.model_dump(exclude_unset=True)
        updated_item = self.repository.update(item_id, **update_data)
        
        return ListItemResponse.from_orm(updated_item)
    
    def delete_item(self, item_id: int, owner_id: int) -> None:
        """Delete a list item"""
        item = self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        # Verify ownership through list
        db_list = self.list_repository.get_by_id_and_owner(item.list_id, owner_id)
        if not db_list:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        self.repository.delete(item_id)
    
    def toggle_item_completion(self, item_id: int, owner_id: int) -> ListItemResponse:
        """Toggle item completion status"""
        item = self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        # Verify ownership through list
        db_list = self.list_repository.get_by_id_and_owner(item.list_id, owner_id)
        if not db_list:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        toggled_item = self.repository.toggle_completion(item_id)
        return ListItemResponse.from_orm(toggled_item)
