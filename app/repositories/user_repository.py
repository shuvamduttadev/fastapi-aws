from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.user import User
from typing import Optional


class UserRepository:
    """Repository for user database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(
        self,
        email: str,
        full_name: str,
        is_active: bool = True,
        is_superuser: bool = False
    ) -> User:
        """Create a new user"""
        db_user = User(
            email=email,
            full_name=full_name,
            hashed_password="AUTH_DISABLED",
            is_active=is_active,
            is_superuser=is_superuser
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 20, is_active: Optional[bool] = None) -> tuple[list[User], int]:
        """Get all users with pagination"""
        query = self.db.query(User)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        total = query.count()
        users = query.order_by(desc(User.created_at)).offset(skip).limit(limit).all()
        
        return users, total
    
    def update(self, user_id: int, **kwargs) -> Optional[User]:
        """Update user information"""
        user = self.get_by_id(user_id)
        if not user:
            return None

        # Update only allowed fields
        allowed_fields = {'email', 'full_name', 'is_active'}
        for key, value in kwargs.items():
            if key in allowed_fields and value is not None:
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """Delete a user"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True
    
