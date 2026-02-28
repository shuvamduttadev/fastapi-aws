from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.v1.user import UserCreateRequest, UserUpdateRequest, UserResponse
from fastapi import HTTPException, status


class UserService:
    """Service for user business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)
    
    def create_user(self, user_data: UserCreateRequest) -> UserResponse:
        """Create a new user with validation"""
        # Check if user already exists
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        user = self.repository.create(
            email=user_data.email,
            full_name=user_data.full_name,
            is_active=user_data.is_active
        )
        
        return UserResponse.model_validate(user)
    
    def get_user(self, user_id: int) -> UserResponse:
        """Get user by ID"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)
    
    def get_users(self, skip: int = 0, limit: int = 20):
        """Get paginated list of users"""
        users, total = self.repository.get_all(skip=skip, limit=limit)
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "items": [UserResponse.model_validate(user) for user in users]
        }
    
    def update_user(self, user_id: int, user_data: UserUpdateRequest) -> UserResponse:
        """Update user information"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if new email already exists (if email is being updated)
        if user_data.email and user_data.email != user.email:
            existing_user = self.repository.get_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists"
                )
        
        update_data = user_data.model_dump(exclude_unset=True)
        updated_user = self.repository.update(user_id, **update_data)
        
        return UserResponse.model_validate(updated_user)
    
    def delete_user(self, user_id: int) -> None:
        """Delete a user"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        self.repository.delete(user_id)
    
