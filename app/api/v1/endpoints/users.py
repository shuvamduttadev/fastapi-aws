from fastapi import APIRouter, Depends, status, Query
from typing import Annotated

from app.db.session import get_db
from app.services.user_service import UserService
from app.schemas.v1.user import (
    UserCreateRequest, UserUpdateRequest, UserResponse, UsersListResponse
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    responses={
        201: {"description": "User created successfully"},
        409: {"description": "User with this email already exists"},
        422: {"description": "Validation error"}
    }
)
def create_user(
    user_data: UserCreateRequest,
    user_service: UserServiceDep
) -> UserResponse:
    """
    Create a new user account.

    - **email**: User email address (must be unique)
    - **full_name**: User full name
    - **is_active**: Whether user account is active (default: true)
    """
    return user_service.create_user(user_data)


@router.get(
    "/",
    response_model=UsersListResponse,
    summary="List all users",
    responses={
        200: {"description": "List of users"}
    }
)
def list_users(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    user_service: UserServiceDep = None
) -> UsersListResponse:
    """
    List all users with pagination.

    - **skip**: Number of users to skip (default: 0)
    - **limit**: Number of users to return (default: 20, max: 100)
    """
    return user_service.get_users(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"}
    }
)
def get_user(
    user_id: int,
    user_service: UserServiceDep
) -> UserResponse:
    """Get user details by ID."""
    return user_service.get_user(user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    responses={
        200: {"description": "User updated successfully"},
        404: {"description": "User not found"},
        409: {"description": "Email already exists"}
    }
)
def update_user(
    user_id: int,
    user_data: UserUpdateRequest,
    user_service: UserServiceDep
) -> UserResponse:
    """
    Update user information.

    - **email**: New email address (optional)
    - **full_name**: New full name (optional)
    - **is_active**: Activate/deactivate account (optional)
    """
    return user_service.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    responses={
        204: {"description": "User deleted successfully"},
        404: {"description": "User not found"}
    }
)
def delete_user(
    user_id: int,
    user_service: UserServiceDep
) -> None:
    """Delete user account."""
    user_service.delete_user(user_id)
