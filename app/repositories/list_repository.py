from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.list import List, ListItem
from typing import Optional


class ListRepository:
    """Repository for list database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, title: str, owner_id: int, description: Optional[str] = None) -> List:
        """Create a new list"""
        db_list = List(
            title=title,
            description=description,
            owner_id=owner_id
        )
        self.db.add(db_list)
        self.db.commit()
        self.db.refresh(db_list)
        return db_list
    
    def get_by_id(self, list_id: int) -> Optional[List]:
        """Get list by ID"""
        return self.db.query(List).filter(List.id == list_id).first()
    
    def get_by_id_and_owner(self, list_id: int, owner_id: int) -> Optional[List]:
        """Get list by ID and owner ID (authorization check)"""
        return self.db.query(List).filter(
            List.id == list_id,
            List.owner_id == owner_id
        ).first()
    
    def get_by_owner(
        self,
        owner_id: int,
        skip: int = 0,
        limit: int = 20,
        is_archived: Optional[bool] = None
    ) -> tuple[list[List], int]:
        """Get all lists for a specific owner"""
        query = self.db.query(List).filter(List.owner_id == owner_id)
        
        if is_archived is not None:
            query = query.filter(List.is_archived == is_archived)
        
        total = query.count()
        lists = query.order_by(desc(List.created_at)).offset(skip).limit(limit).all()
        
        return lists, total
    
    def update(self, list_id: int, **kwargs) -> Optional[List]:
        """Update list information"""
        db_list = self.get_by_id(list_id)
        if not db_list:
            return None
        
        allowed_fields = {'title', 'description', 'is_archived'}
        for key, value in kwargs.items():
            if key in allowed_fields and value is not None:
                setattr(db_list, key, value)
        
        self.db.commit()
        self.db.refresh(db_list)
        return db_list
    
    def delete(self, list_id: int) -> bool:
        """Delete a list"""
        db_list = self.get_by_id(list_id)
        if not db_list:
            return False
        
        self.db.delete(db_list)
        self.db.commit()
        return True
    
    def archive(self, list_id: int) -> Optional[List]:
        """Archive a list"""
        return self.update(list_id, is_archived=True)
    
    def unarchive(self, list_id: int) -> Optional[List]:
        """Unarchive a list"""
        return self.update(list_id, is_archived=False)


class ListItemRepository:
    """Repository for list item database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, list_id: int, content: str, order: int = 0) -> ListItem:
        """Create a new list item"""
        item = ListItem(
            list_id=list_id,
            content=content,
            order=order
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def get_by_id(self, item_id: int) -> Optional[ListItem]:
        """Get list item by ID"""
        return self.db.query(ListItem).filter(ListItem.id == item_id).first()
    
    def get_by_list(self, list_id: int) -> list[ListItem]:
        """Get all items in a list"""
        return self.db.query(ListItem).filter(ListItem.list_id == list_id).order_by(ListItem.order).all()
    
    def update(self, item_id: int, **kwargs) -> Optional[ListItem]:
        """Update list item"""
        item = self.get_by_id(item_id)
        if not item:
            return None
        
        allowed_fields = {'content', 'is_completed', 'order'}
        for key, value in kwargs.items():
            if key in allowed_fields and value is not None:
                setattr(item, key, value)
        
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete(self, item_id: int) -> bool:
        """Delete a list item"""
        item = self.get_by_id(item_id)
        if not item:
            return False
        
        self.db.delete(item)
        self.db.commit()
        return True
    
    def toggle_completion(self, item_id: int) -> Optional[ListItem]:
        """Toggle item completion status"""
        item = self.get_by_id(item_id)
        if not item:
            return None
        
        item.is_completed = not item.is_completed
        self.db.commit()
        self.db.refresh(item)
        return item
