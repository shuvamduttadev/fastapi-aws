# FastAPI Enterprise CRUD System - Complete Documentation

## Overview

This is a professional, enterprise-level FastAPI application featuring a complete CRUD flow for managing users and lists with items. The project follows industry best practices including proper architecture patterns, data validation, authentication, authorization, rate limiting, and database migrations.

## Project Structure

```
app/
├── __init__.py
├── main.py                          # FastAPI application entry point
├── api/
│   └── v1/
│       ├── api.py                   # API router configuration
│       ├── deps.py                  # Dependency injection
│       └── endpoints/
│           ├── users.py             # User CRUD endpoints
│           └── lists.py             # List and item CRUD endpoints
├── core/
│   ├── config.py                    # Configuration settings
│   ├── security.py                  # Password hashing & JWT tokens
│   ├── dependencies.py              # Dependency providers
│   ├── exceptions.py                # Exception handlers
│   └── logging.py                   # Logging configuration
├── db/
│   ├── base.py                      # Database base with all models
│   ├── base_class.py                # SQLAlchemy base class
│   └── session.py                   # Database session management
├── models/
│   ├── user.py                      # User database model
│   └── list.py                      # List and ListItem models
├── repositories/
│   ├── user_repository.py           # User data access
│   └── list_repository.py           # List & ListItem data access
├── services/
│   ├── user_service.py              # User business logic
│   └── list_service.py              # List business logic
├── schemas/
│   └── v1/
│       ├── user.py                  # User Pydantic schemas
│       └── list.py                  # List Pydantic schemas
└── utils/
    ├── helpers.py                   # Utility functions
    └── rate_limiter.py              # Rate limiting configuration

alembic/                             # Database migrations
├── env.py                           # Migration environment
├── script.py.mako                   # Migration template
└── versions/
    ├── 001_initial.py               # Initial database schema
    └── __init__.py

requirements.txt                     # Python dependencies
```

## Core Features

### 1. User Management (CRUD)
- ✅ Create new user accounts with validation
- ✅ Read/retrieve user profiles
- ✅ Update user information
- ✅ Delete user accounts
- ✅ Activate/Deactivate user accounts
- ✅ Last login tracking

**User Endpoints:**
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/` - List all users (superuser only)
- `GET /api/v1/users/{user_id}` - Get user details
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user
- `POST /api/v1/users/{user_id}/deactivate` - Deactivate user
- `POST /api/v1/users/{user_id}/activate` - Activate user (superuser)

### 2. List Management (CRUD)
- ✅ Create lists with titles and descriptions
- ✅ Read/retrieve lists with metadata
- ✅ Update list information
- ✅ Delete lists (cascade deletes items)
- ✅ Archive/Unarchive lists
- ✅ User ownership enforcement

**List Endpoints:**
- `POST /api/v1/lists/` - Create list
- `GET /api/v1/lists/` - Get user's lists
- `GET /api/v1/lists/{list_id}` - Get list with items
- `PUT /api/v1/lists/{list_id}` - Update list
- `DELETE /api/v1/lists/{list_id}` - Delete list
- `POST /api/v1/lists/{list_id}/archive` - Archive list
- `POST /api/v1/lists/{list_id}/unarchive` - Unarchive list

### 3. List Items Management (CRUD)
- ✅ Add items to lists
- ✅ Read/retrieve items
- ✅ Update item content and status
- ✅ Delete items
- ✅ Toggle completion status
- ✅ Item ordering support

**ListItem Endpoints:**
- `POST /api/v1/lists/{list_id}/items` - Create item
- `GET /api/v1/lists/{list_id}/items` - Get all items
- `GET /api/v1/lists/{list_id}/items/{item_id}` - Get item
- `PUT /api/v1/lists/{list_id}/items/{item_id}` - Update item
- `DELETE /api/v1/lists/{list_id}/items/{item_id}` - Delete item
- `POST /api/v1/lists/{list_id}/items/{item_id}/toggle` - Toggle completion

## Schema Validation

### Request/Response Models (Pydantic)

All endpoints use Pydantic models for:
- Request body validation
- Response serialization
- Automatic OpenAPI documentation
- Type safety and IDE support

**User Schemas:**
- `UserCreateRequest` - Create user validation
- `UserUpdateRequest` - Update user validation
- `UserResponse` - User response formatting
- `UsersListResponse` - Paginated users response

**List Schemas:**
- `ListCreateRequest` - Create list validation
- `ListUpdateRequest` - Update list validation
- `ListResponse` - List response formatting
- `ListDetailResponse` - List with items response
- `ListsListResponse` - Paginated lists response

**ListItem Schemas:**
- `ListItemCreateRequest` - Create item validation
- `ListItemUpdateRequest` - Update item validation
- `ListItemResponse` - Item response formatting

### Validation Features

1. **Field Validation**
   - Email validation (using `email-validator`)
   - Password strength requirements:
     - Minimum 8 characters
     - At least one uppercase letter
     - At least one lowercase letter
     - At least one digit
   - String length constraints
   - Numeric range validation

2. **Custom Validators**
   - Password complexity validation
   - Email uniqueness checks
   - User ownership verification

## Database Models & Migrations

### Models

**User Model**
```python
- id (PK)
- email (unique)
- full_name
- hashed_password
- is_active
- is_superuser
- created_at
- updated_at
- last_login
- relationships: lists
```

**List Model**
```python
- id (PK)
- title
- description
- owner_id (FK → users.id)
- is_archived
- created_at
- updated_at
- relationships: owner, items
```

**ListItem Model**
```python
- id (PK)
- list_id (FK → lists.id)
- content
- is_completed
- order
- created_at
- updated_at
- relationships: list
```

### Migrations (Alembic)

The project uses Alembic for database schema management.

**Running Migrations:**

```bash
# Upgrade to latest version
alembic upgrade head

# Downgrade to previous version
alembic downgrade -1

# Create new migration (auto-generated)
alembic revision --autogenerate -m "Description"

# View migration history
alembic history

# Current version
alembic current
```

**Initial Migration:** `001_initial.py`
- Creates users, lists, and list_items tables
- Defines foreign key relationships with CASCADE delete
- Creates indexes for performance optimization

## Authentication & Authorization

### JWT Token-Based Authentication

1. **Token Generation**
   - Tokens generated via `/auth/token` endpoint (external)
   - Default expiry: 30 minutes
   - Uses HS256 algorithm

2. **Token Validation**
   - All protected endpoints require valid JWT token
   - Token passed via `Authorization: Bearer {token}` header
   - Automatic user lookup from token claims

3. **Authorization**
   - Role-based access control (RBAC)
   - Superuser permissions for admin operations
   - User ownership verification for resource access
   - Custom permission decorators available

### Dependency Injection

```python
# Current user from token
CurrentUser = Annotated[User, Depends(get_current_user)]

# Service dependencies
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
ListServiceDep = Annotated[ListService, Depends(get_list_service)]
ListItemServiceDep = Annotated[ListItemService, Depends(get_list_item_service)]
```

## Rate Limiting

### Configuration

```python
# In core/config.py
RATE_LIMIT_ENABLED = True
RATE_LIMIT_DEFAULT = "100/minute"
RATE_LIMIT_AUTH = "30/minute"
```

### Implementation

Using `slowapi` middleware:
- Default limit: 100 requests per minute
- Auth stricter limit: 30 requests per minute
- Rate limit by IP address (remote address)
- Configurable per endpoint

**Example usage:**
```python
from app.utils.rate_limiter import limiter

@app.get("/endpoint")
@limiter.limit("5/minute")
async def limited_endpoint():
    pass
```

## CORS Configuration

### Settings

```python
# In core/config.py
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]
```

### Setup

CORS middleware automatically configured in `main.py`:
- Handles preflight requests
- Allows credentials (cookies, auth headers)
- Configurable for production domains

## Error Handling

### Custom Exception Handlers

1. **ValidationError** - Returns detailed field validation errors
2. **HTTPException** - Returns standardized error responses
3. **Database Errors** - Automatically converted to API errors

### Error Response Format

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

## Repository Pattern

### Benefits
- Decouples business logic from data access
- Easier testing with mock repositories
- Consistent data access patterns
- Query optimization in one place

### Repositories Implemented

1. **UserRepository**
   - CRUD operations
   - Authentication
   - User status management

2. **ListRepository**
   - CRUD operations
   - Archive/Unarchive
   - Owner filtering

3. **ListItemRepository**
   - CRUD operations
   - Item ordering
   - Completion status management

## Service Layer

### Benefits
- Centralized business logic
- Validation and error handling
- Transaction management
- Authorization checks

### Services Implemented

1. **UserService**
   - User creation with validation
   - Profile management
   - Account activation/deactivation

2. **ListService**
   - List creation and management
   - Archive operations
   - User-based filtering

3. **ListItemService**
   - Item management with ownership checks
   - Completion toggling
   - List-based filtering

## Pagination

### Implementation

Query parameters for pagination:
- `skip` (default: 0) - Items to skip
- `limit` (default: 20, max: 100) - Items per page

**Example:**
```
GET /api/v1/users/?skip=0&limit=20
```

### Response Format

```json
{
  "total": 100,
  "skip": 0,
  "limit": 20,
  "items": [...]
}
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip or poetry

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Initialize database**
   ```bash
   alembic upgrade head
   ```

4. **Run application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Logging
LOG_LEVEL=INFO
```

## Testing

### Test Coverage

Tests should cover:
- ✅ User CRUD operations
- ✅ List CRUD operations
- ✅ ListItem CRUD operations
- ✅ Authentication flow
- ✅ Authorization/permissions
- ✅ Validation errors
- ✅ Edge cases (duplicate email, cascading deletes, etc.)

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_users.py

# With coverage
pytest --cov=app
```

## API Documentation

### Auto-generated Docs

1. **Swagger UI**: http://localhost:8000/api/docs
2. **ReDoc**: http://localhost:8000/api/redoc
3. **OpenAPI JSON**: http://localhost:8000/api/openapi.json

### Implementation

All endpoints include:
- ✅ Detailed docstrings
- ✅ Parameter descriptions
- ✅ Response schemas
- ✅ Example values
- ✅ HTTP status codes
- ✅ Error descriptions

## Best Practices Implemented

1. **Code Organization**
   - Separation of concerns (routers, services, repositories)
   - DRY principle with shared utilities
   - Clear module responsibilities

2. **Data Validation**
   - Input validation at endpoint level
   - Database constraint enforcement
   - Custom validator implementations

3. **Security**
   - Password hashing with bcrypt
   - JWT token-based authentication
   - Authorization on sensitive operations
   - Rate limiting for DOS protection
   - CORS protection

4. **Database**
   - Migrations for schema versioning
   - Foreign key constraints with cascading
   - Indexes on frequently queried columns
   - Timestamp tracking (created_at, updated_at)

5. **API Design**
   - RESTful endpoint design
   - Proper HTTP status codes
   - Consistent error responses
   - Pagination for list endpoints
   - Clear resource naming

6. **Documentation**
   - Comprehensive docstrings
   - Auto-generated API docs
   - Type hints throughout
   - Example usage

## Future Enhancements

- [ ] WebSocket support for real-time updates
- [ ] File attachment uploads
- [ ] Sharing lists with other users
- [ ] Due dates and reminders
- [ ] List templates
- [ ] Advanced filtering and search
- [ ] Activity logging/audit trail
- [ ] Email notifications
- [ ] Two-factor authentication
- [ ] API key authentication option

## Performance Considerations

1. **Database Indexes**
   - Email (unique)
   - User ID (foreign key)
   - List title (search)
   - Creation dates (sorting)

2. **Query Optimization**
   - Eager loading of relationships
   - Pagination for large datasets
   - Selective field queries

3. **Caching**
   - Redis integration ready
   - User session caching
   - Rate limit storage

## Deployment

### Docker

Dockerfile and docker-compose.yml included for easy deployment.

### Production Checklist

- [ ] Update `SECRET_KEY` in environment
- [ ] Configure correct `DATABASE_URL`
- [ ] Update `CORS_ORIGINS` for production domain
- [ ] Enable HTTPS
- [ ] Set up log aggregation
- [ ] Configure monitoring/alerting
- [ ] Run database backups
- [ ] Security audit

## Contributing

### Code Style
- Follow PEP 8
- Use type hints
- Write docstrings
- Add tests for new features

### Pull Request Process
1. Create feature branch
2. Make changes
3. Add tests
4. Update documentation
5. Submit PR with description

## License

[Your License Here]

## Support

For issues and questions:
- GitHub Issues
- Email: support@example.com
- Documentation: http://localhost:8000/api/docs
