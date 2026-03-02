# FastAPI Lists API - Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env` file

```bash
cp .env.example .env
# Edit .env with your actual values
```

### 3. Database Setup

```bash
# Run migrations
alembic upgrade head

# Or initialize from scratch (if no migrations exist)
alembic upgrade head
```

### 4. Run the Application

```bash
# Development with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Project Structure

### Key Components

1. **Models** (`app/models/`)
   - User: User account model
   - List: Todo list model
   - ListItem: List item model

2. **Schemas** (`app/schemas/v1/`)
   - Input validation (Request models)
   - Output serialization (Response models)

3. **Repositories** (`app/repositories/`)
   - Data access layer
   - CRUD operations
   - Query building

4. **Services** (`app/services/`)
   - Business logic
   - Validation
   - Authorization checks

5. **Endpoints** (`app/api/v1/endpoints/`)
   - HTTP route handlers
   - Request/response processing

## API Endpoints

### Users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/` - List users (superuser)
- `GET /api/v1/users/{id}` - Get user
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user
- `POST /api/v1/users/{id}/deactivate` - Deactivate
- `POST /api/v1/users/{id}/activate` - Activate (superuser)

### Lists
- `POST /api/v1/lists/` - Create list
- `GET /api/v1/lists/` - Get user's lists
- `GET /api/v1/lists/{id}` - Get list with items
- `PUT /api/v1/lists/{id}` - Update list
- `DELETE /api/v1/lists/{id}` - Delete list
- `POST /api/v1/lists/{id}/archive` - Archive list
- `POST /api/v1/lists/{id}/unarchive` - Unarchive list

### List Items
- `POST /api/v1/lists/{list_id}/items` - Create item
- `GET /api/v1/lists/{list_id}/items` - Get all items
- `GET /api/v1/lists/{list_id}/items/{item_id}` - Get item
- `PUT /api/v1/lists/{list_id}/items/{item_id}` - Update item
- `DELETE /api/v1/lists/{list_id}/items/{item_id}` - Delete item
- `POST /api/v1/lists/{list_id}/items/{item_id}/toggle` - Toggle completion

## Features

### Authentication
- JWT token-based authentication
- Password hashing with bcrypt
- Token expiration and refresh

### Authorization
- User ownership verification
- Role-based access control (superuser)
- Resource-level permissions

### Validation
- Pydantic schema validation
- Custom validators
- Password strength requirements
- Email validation

### Rate Limiting
- slowapi integration
- Configurable per-endpoint limits
- IP-based rate limiting

### CORS
- Automatic CORS middleware
- Configurable allowed origins
- Credentials support

### Database
- SQLAlchemy ORM
- Alembic migrations
- PostgreSQL support
- Foreign key constraints
- Cascading deletes

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000"]
CORS_CREDENTIALS=true
CORS_METHODS=["*"]
CORS_HEADERS=["*"]

# Rate Limiting
RATE_LIMIT_DEFAULT=100/minute
RATE_LIMIT_AUTH=30/minute

# Logging
LOG_LEVEL=INFO
```

## Development

### Running Tests

```bash
pytest
pytest tests/test_users.py -v
pytest --cov=app
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# View history
alembic history
```

### Code Style

```bash
# Format code
black app

# Check style
flake8 app

# Type checking
mypy app
```

## Production Deployment

### Docker

```bash
docker-compose up -d
```

### Cloud Platforms

- **AWS ECS**: See `deployment/aws-ecs/`
- **AWS Lambda**: See `deployment/aws-lambda/`
- **AWS Beanstalk**: See `deployment/aws-beanstalk/`

### Pre-deployment Checklist

- [ ] Update SECRET_KEY
- [ ] Configure DATABASE_URL for production
- [ ] Update CORS_ORIGINS
- [ ] Enable HTTPS
- [ ] Set LOG_LEVEL to WARNING
- [ ] Configure monitoring
- [ ] Set up backups
- [ ] Security audit

## Troubleshooting

### Database Connection Error
```
Check DATABASE_URL in .env
Ensure PostgreSQL is running
Verify database exists
```

### Import Errors
```
Reinstall dependencies: pip install -r requirements.txt
Check PYTHONPATH includes project root
```

### Migration Issues
```
# Reset to initial state
alembic downgrade base
alembic upgrade head

# Auto-generate from models
alembic revision --autogenerate -m "Sync with models"
```

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org
- **Alembic Documentation**: https://alembic.sqlalchemy.org
- **Pydantic Documentation**: https://docs.pydantic.dev

## Support

For issues and questions, refer to:
- `API_DOCUMENTATION.md` - Complete API reference
- `README.md` - Project overview
- GitHub Issues - Bug reports and features
