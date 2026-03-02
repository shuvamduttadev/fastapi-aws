# API Quick Reference

## Base URL
```
http://localhost:8000
```

## Authentication
All endpoints except user creation and health check require JWT token in header:
```
Authorization: Bearer {token}
```

## Response Format
### Success (2xx)
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  ...
}
```

### Error (4xx, 5xx)
```json
{
  "success": false,
  "error": "Error type",
  "details": [
    {
      "field": "field_name",
      "message": "Error message"
    }
  ]
}
```

## User Endpoints

### Create User
```
POST /api/v1/users/

Request:
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "SecurePass123",
  "is_active": true
}

Response: 201
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "last_login": null
}
```

### List All Users
```
GET /api/v1/users/?skip=0&limit=20

Headers:
Authorization: Bearer {token}

Response: 200
{
  "total": 100,
  "skip": 0,
  "limit": 20,
  "items": [...]
}

Note: Requires superuser role
```

### Get User by ID
```
GET /api/v1/users/{user_id}

Headers:
Authorization: Bearer {token}

Response: 200
{
  "id": 1,
  "email": "user@example.com",
  ...
}
```

### Get Current User
```
GET /api/v1/users/me

Headers:
Authorization: Bearer {token}

Response: 200
{
  "id": 1,
  "email": "user@example.com",
  ...
}
```

### Update User
```
PUT /api/v1/users/{user_id}

Headers:
Authorization: Bearer {token}

Request:
{
  "email": "newemail@example.com",
  "full_name": "New Name",
  "is_active": true
}

Response: 200
{...updated user...}
```

### Delete User
```
DELETE /api/v1/users/{user_id}

Headers:
Authorization: Bearer {token}

Response: 204 (No Content)
```

### Deactivate User
```
POST /api/v1/users/{user_id}/deactivate

Headers:
Authorization: Bearer {token}

Response: 200
{...deactivated user...}
```

### Activate User
```
POST /api/v1/users/{user_id}/activate

Headers:
Authorization: Bearer {token}

Response: 200
{...activated user...}

Note: Requires superuser role
```

## List Endpoints

### Create List
```
POST /api/v1/lists/

Headers:
Authorization: Bearer {token}

Request:
{
  "title": "Shopping",
  "description": "Weekly groceries",
  "is_archived": false
}

Response: 201
{
  "id": 1,
  "owner_id": 1,
  "title": "Shopping",
  "description": "Weekly groceries",
  "is_archived": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Get User's Lists
```
GET /api/v1/lists/?skip=0&limit=20

Headers:
Authorization: Bearer {token}

Response: 200
{
  "total": 10,
  "skip": 0,
  "limit": 20,
  "items": [...]
}
```

### Get List with Items
```
GET /api/v1/lists/{list_id}

Headers:
Authorization: Bearer {token}

Response: 200
{
  "id": 1,
  "owner_id": 1,
  "title": "Shopping",
  "description": "Weekly groceries",
  "is_archived": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "items": [
    {
      "id": 1,
      "list_id": 1,
      "content": "Milk",
      "is_completed": false,
      "order": 0,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ]
}
```

### Update List
```
PUT /api/v1/lists/{list_id}

Headers:
Authorization: Bearer {token}

Request:
{
  "title": "Updated Shopping",
  "description": "Updated description",
  "is_archived": false
}

Response: 200
{...updated list...}
```

### Delete List
```
DELETE /api/v1/lists/{list_id}

Headers:
Authorization: Bearer {token}

Response: 204 (No Content)

Note: Cascades delete to all items
```

### Archive List
```
POST /api/v1/lists/{list_id}/archive

Headers:
Authorization: Bearer {token}

Response: 200
{...archived list...}
```

### Unarchive List
```
POST /api/v1/lists/{list_id}/unarchive

Headers:
Authorization: Bearer {token}

Response: 200
{...unarchived list...}
```

## List Item Endpoints

### Create Item
```
POST /api/v1/lists/{list_id}/items

Headers:
Authorization: Bearer {token}

Request:
{
  "content": "Buy milk",
  "is_completed": false,
  "order": 0
}

Response: 201
{
  "id": 1,
  "list_id": 1,
  "content": "Buy milk",
  "is_completed": false,
  "order": 0,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Get List Items
```
GET /api/v1/lists/{list_id}/items

Headers:
Authorization: Bearer {token}

Response: 200
[
  {
    "id": 1,
    "list_id": 1,
    "content": "Buy milk",
    "is_completed": false,
    "order": 0,
    ...
  }
]
```

### Get Item
```
GET /api/v1/lists/{list_id}/items/{item_id}

Headers:
Authorization: Bearer {token}

Response: 200
{
  "id": 1,
  "list_id": 1,
  "content": "Buy milk",
  ...
}
```

### Update Item
```
PUT /api/v1/lists/{list_id}/items/{item_id}

Headers:
Authorization: Bearer {token}

Request:
{
  "content": "Buy 2L milk",
  "is_completed": false,
  "order": 0
}

Response: 200
{...updated item...}
```

### Delete Item
```
DELETE /api/v1/lists/{list_id}/items/{item_id}

Headers:
Authorization: Bearer {token}

Response: 204 (No Content)
```

### Toggle Item Completion
```
POST /api/v1/lists/{list_id}/items/{item_id}/toggle

Headers:
Authorization: Bearer {token}

Response: 200
{
  "id": 1,
  "list_id": 1,
  "content": "Buy milk",
  "is_completed": true,  # Changed from false
  ...
}
```

## Status/Health Endpoints

### Root
```
GET /

Response: 200
{
  "message": "Welcome to FastAPI Lists API!",
  "version": "1.0.0",
  "environment": "development",
  "documentation": "/api/docs"
}
```

### Health Check
```
GET /health

Response: 200
{
  "status": "healthy",
  "message": "FastAPI Lists API service is healthy!",
  "version": "1.0.0",
  "database": "connected",
  "timestamp": "2024-01-01T00:00:00"
}
```

### API Status
```
GET /api/v1/status

Response: 200
{
  "status": "operational",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00"
}
```

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created |
| 204 | No Content - Successful deletion |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Token required/invalid |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Duplicate resource |
| 422 | Validation Error - Invalid data |
| 429 | Too Many Requests - Rate limited |
| 500 | Server Error - Internal error |
| 503 | Service Unavailable - Database down |

## Query Parameters

### Pagination
```
skip=0      # Number of items to skip (default: 0)
limit=20    # Number of items per page (default: 20, max: 100)
```

### Examples
```bash
# Get users 20-40
GET /api/v1/users/?skip=20&limit=20

# Get first 50 lists
GET /api/v1/lists/?skip=0&limit=50
```

## Common Errors

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```
**Fix**: Ensure token is valid and not expired

### 403 Forbidden
```json
{
  "detail": "Cannot update other users"
}
```
**Fix**: Must own the resource or be superuser

### 404 Not Found
```json
{
  "detail": "User not found"
}
```
**Fix**: Check if ID is correct

### 409 Conflict
```json
{
  "detail": "User with this email already exists"
}
```
**Fix**: Email is already registered

### 422 Validation Error
```json
{
  "success": false,
  "error": "Validation Error",
  "details": [
    {
      "field": "password",
      "message": "Password must contain at least one uppercase letter"
    }
  ]
}
```
**Fix**: Check field requirements

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```
**Fix**: Wait before making next request

## Password Requirements
- Minimum 8 characters
- Maximum **72 bytes** (bcrypt limitation; characters beyond this are truncated)
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)

Example: `SecurePass123`

> Note: bcrypt only processes the first 72 bytes of the password. Very long
> strings will be silently truncated during hashing.
## Rate Limits
- Default: 100 requests per minute
- Auth endpoints: 30 requests per minute

## Testing with curl

```bash
# Create user
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"TestPass123"}'

# Get health
curl http://localhost:8000/health

# With authentication
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/users/me
```

## API Documentation
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- OpenAPI JSON: http://localhost:8000/api/openapi.json
