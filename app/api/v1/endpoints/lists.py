from fastapi import APIRouter, HTTPException, status, Query
from typing import Annotated

from app.api.v1.deps import ListServiceDep, ListItemServiceDep, CurrentUser
from app.schemas.v1.list import (
    ListCreateRequest, ListUpdateRequest, ListResponse, ListDetailResponse, ListsListResponse,
    ListItemCreateRequest, ListItemUpdateRequest, ListItemResponse
)

router = APIRouter(prefix="/lists", tags=["lists"])


# ============================================================================
# List Endpoints
# ============================================================================

@router.post(
    "/",
    response_model=ListResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new list",
    responses={
        201: {"description": "List created successfully"},
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"}
    }
)
async def create_list(
    list_data: ListCreateRequest,
    list_service: ListServiceDep,
    current_user: CurrentUser
) -> ListResponse:
    """
    Create a new list for the current user.
    
    Requires authentication.
    
    - **title**: List title (required)
    - **description**: List description (optional)
    - **is_archived**: Whether list is archived (default: false)
    """
    return list_service.create_list(current_user.id, list_data)


@router.get(
    "/",
    response_model=ListsListResponse,
    summary="List user's lists",
    responses={
        200: {"description": "List of user's lists"},
        401: {"description": "Unauthorized"}
    }
)
async def get_user_lists(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    list_service: ListServiceDep = None,
    current_user: CurrentUser = None
) -> ListsListResponse:
    """
    Get all lists for the current user with pagination.
    
    Requires authentication.
    
    - **skip**: Number of lists to skip (default: 0)
    - **limit**: Number of lists to return (default: 20, max: 100)
    """
    return list_service.get_user_lists(current_user.id, skip=skip, limit=limit)


@router.get(
    "/{list_id}",
    response_model=ListDetailResponse,
    summary="Get list with items",
    responses={
        200: {"description": "List found"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "List not found"}
    }
)
async def get_list(
    list_id: int,
    list_service: ListServiceDep,
    current_user: CurrentUser
) -> ListDetailResponse:
    """
    Get list details with all its items.
    
    Requires authentication. Users can only access their own lists.
    """
    return list_service.get_list(list_id, owner_id=current_user.id)


@router.put(
    "/{list_id}",
    response_model=ListResponse,
    summary="Update list",
    responses={
        200: {"description": "List updated successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "List not found"},
        422: {"description": "Validation error"}
    }
)
async def update_list(
    list_id: int,
    list_data: ListUpdateRequest,
    list_service: ListServiceDep,
    current_user: CurrentUser
) -> ListResponse:
    """
    Update list information.
    
    Requires authentication. Users can only update their own lists.
    
    - **title**: New list title (optional)
    - **description**: New list description (optional)
    - **is_archived**: Archive/unarchive list (optional)
    """
    return list_service.update_list(list_id, current_user.id, list_data)


@router.delete(
    "/{list_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete list",
    responses={
        204: {"description": "List deleted successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "List not found"}
    }
)
async def delete_list(
    list_id: int,
    list_service: ListServiceDep,
    current_user: CurrentUser
) -> None:
    """
    Delete a list.
    
    Requires authentication. Users can only delete their own lists.
    Deleting a list will also delete all items in it.
    """
    list_service.delete_list(list_id, current_user.id)


@router.post(
    "/{list_id}/archive",
    response_model=ListResponse,
    summary="Archive list",
    responses={
        200: {"description": "List archived"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "List not found"}
    }
)
async def archive_list(
    list_id: int,
    list_service: ListServiceDep,
    current_user: CurrentUser
) -> ListResponse:
    """
    Archive a list.
    
    Requires authentication. Users can only archive their own lists.
    Archived lists are hidden by default but can be restored.
    """
    return list_service.archive_list(list_id, current_user.id)


@router.post(
    "/{list_id}/unarchive",
    response_model=ListResponse,
    summary="Unarchive list",
    responses={
        200: {"description": "List unarchived"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "List not found"}
    }
)
async def unarchive_list(
    list_id: int,
    list_service: ListServiceDep,
    current_user: CurrentUser
) -> ListResponse:
    """
    Unarchive a list.
    
    Requires authentication. Users can only unarchive their own lists.
    """
    return list_service.unarchive_list(list_id, current_user.id)


# ============================================================================
# List Item Endpoints
# ============================================================================

@router.post(
    "/{list_id}/items",
    response_model=ListItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add item to list",
    responses={
        201: {"description": "Item created successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "List not found"},
        422: {"description": "Validation error"}
    }
)
async def create_list_item(
    list_id: int,
    item_data: ListItemCreateRequest,
    list_item_service: ListItemServiceDep,
    current_user: CurrentUser
) -> ListItemResponse:
    """
    Add a new item to a list.
    
    Requires authentication. Users can only add items to their own lists.
    
    - **content**: Item content/text (required)
    - **is_completed**: Whether item is completed (default: false)
    - **order**: Item order in the list (default: 0)
    """
    return list_item_service.create_item(list_id, current_user.id, item_data)


@router.get(
    "/{list_id}/items",
    response_model=list[ListItemResponse],
    summary="Get list items",
    responses={
        200: {"description": "List items"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "List not found"}
    }
)
async def get_list_items(
    list_id: int,
    list_item_service: ListItemServiceDep,
    current_user: CurrentUser
) -> list[ListItemResponse]:
    """
    Get all items in a list.
    
    Requires authentication. Users can only view items in their own lists.
    Items are returned in order.
    """
    return list_item_service.get_list_items(list_id, current_user.id)


@router.get(
    "/{list_id}/items/{item_id}",
    response_model=ListItemResponse,
    summary="Get list item",
    responses={
        200: {"description": "Item found"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Item not found"}
    }
)
async def get_list_item(
    list_id: int,
    item_id: int,
    list_item_service: ListItemServiceDep,
    current_user: CurrentUser
) -> ListItemResponse:
    """
    Get a specific item from a list.
    
    Requires authentication. Users can only access items in their own lists.
    """
    return list_item_service.get_item(item_id, current_user.id)


@router.put(
    "/{list_id}/items/{item_id}",
    response_model=ListItemResponse,
    summary="Update list item",
    responses={
        200: {"description": "Item updated successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Item not found"},
        422: {"description": "Validation error"}
    }
)
async def update_list_item(
    list_id: int,
    item_id: int,
    item_data: ListItemUpdateRequest,
    list_item_service: ListItemServiceDep,
    current_user: CurrentUser
) -> ListItemResponse:
    """
    Update a list item.
    
    Requires authentication. Users can only update items in their own lists.
    
    - **content**: New item content (optional)
    - **is_completed**: Update completion status (optional)
    - **order**: Update item order (optional)
    """
    return list_item_service.update_item(item_id, current_user.id, item_data)


@router.delete(
    "/{list_id}/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete list item",
    responses={
        204: {"description": "Item deleted successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Item not found"}
    }
)
async def delete_list_item(
    list_id: int,
    item_id: int,
    list_item_service: ListItemServiceDep,
    current_user: CurrentUser
) -> None:
    """
    Delete an item from a list.
    
    Requires authentication. Users can only delete items from their own lists.
    """
    list_item_service.delete_item(item_id, current_user.id)


@router.post(
    "/{list_id}/items/{item_id}/toggle",
    response_model=ListItemResponse,
    summary="Toggle item completion",
    responses={
        200: {"description": "Item completion toggled"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Item not found"}
    }
)
async def toggle_item_completion(
    list_id: int,
    item_id: int,
    list_item_service: ListItemServiceDep,
    current_user: CurrentUser
) -> ListItemResponse:
    """
    Toggle completion status of a list item.
    
    Requires authentication. Users can only toggle items in their own lists.
    Converts completed items to incomplete and vice versa.
    """
    return list_item_service.toggle_item_completion(item_id, current_user.id)
