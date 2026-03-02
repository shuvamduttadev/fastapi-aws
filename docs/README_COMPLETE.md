# FastAPI Enterprise-Level CRUD Application

A professional, production-ready FastAPI application implementing a complete CRUD flow for managing users and to-do lists. Built with enterprise-level best practices including proper architecture patterns, validation, authentication, authorization, rate limiting, and database migrations.

## 🎯 Project Overview

This application demonstrates a fully-functional backend system with:
- **User Management**: Complete CRUD operations with authentication
- **List Management**: Create, read, update, delete personal to-do lists
- **List Items**: Manage items within lists with status tracking
- **Security**: JWT authentication, password hashing, CORS protection
- **Database**: SQLAlchemy ORM with Alembic migrations
- **Validation**: Pydantic schemas with custom validators
- **Rate Limiting**: slowapi integration for DOS protection
- **Documentation**: Auto-generated API docs with Swagger UI

## 🚀 Features

### Core Features
✅ User registration and management  
✅ JWT-based authentication  
✅ Password strength validation  
✅ User account activation/deactivation  
✅ Create and manage multiple lists  
✅ Add/edit/delete items in lists  
✅ Mark items as complete/incomplete  
✅ Archive/unarchive lists  
✅ User ownership verification  
✅ Superuser role for administration  

### Technical Features
✅ RESTful API design  
✅ Request/response validation with Pydantic  
✅ Database migrations with Alembic  
✅ Rate limiting (slowapi)  
✅ CORS middleware  
✅ Comprehensive error handling  
✅ Pagination support  
✅ Type hints throughout  
✅ Detailed API documentation  
✅ Repository and Service layers  

## 📁 Project Structure

```
fastapi/
├── app/
│   ├── api/v1/                      # API v1 routes
│   │   ├── endpoints/
│   │   │   ├── users.py             # User CRUD endpoints
│   │   │   └── lists.py             # List/Item CRUD endpoints
│   │   ├── api.py                   # Router configuration
│   │   └── deps.py                  # Dependency injection
│   ├── core/                        # Core configuration
│   │   ├── config.py                # Settings & env vars
│   │   ├── security.py              # JWT & password hashing
│   │   ├── dependencies.py          # Auth dependencies
│   │   ├── exceptions.py            # Error handlers
│   │   └── logging.py               # Logging setup
│   ├── db/                          # Database
│   │   ├── base.py                  # Model imports
│   │   ├── base_class.py            # SQLAlchemy base
│   │   └── session.py               # DB session
│   ├── models/                      # Data models
│   │   ├── user.py                  # User model
│   │   └── list.py                  # List & ListItem
│   ├── repositories/                # Data access layer
│   │   ├── user_repository.py
│   │   └── list_repository.py
│   ├── services/                    # Business logic
│   │   ├── user_service.py
│   │   └── list_service.py
│   ├── schemas/v1/                  # Pydantic models
│   │   ├── user.py
│   │   └── list.py
│   ├── utils/                       # Utilities
│   │   └── rate_limiter.py
│   └── main.py                      # FastAPI app entry
├── alembic/                         # Database migrations
│   ├── versions/
│   │   └── 001_initial.py           # Initial schema
│   ├── env.py
│   └── script.py.mako
├── tests/                           # Test suite
├── requirements.txt                 # Dependencies
├── .env.example                     # Environment template
├── init_db.py                       # Database initialization
├── API_DOCUMENTATION.md             # API reference
├── SETUP_GUIDE.md                   # Installation guide
└── README.md                        # This file
```

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.128.0
- **Database**: PostgreSQL with SQLAlchemy 2.0
- **Migrations**: Alembic 1.12.0
- **Validation**: Pydantic 2.12.5
- **Authentication**: Python-Jose, Passlib
- **Rate Limiting**: slowapi 0.1.9
- **Server**: Uvicorn 0.23.2
- **HTTP Client**: Python Requests

## 📦 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip

### Setup

1. **Clone and navigate to project**
   ```bash
   cd fastapi
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Initialize database**
   ```bash
   python init_db.py
   # or with Alembic: alembic upgrade head
   ```

6. **Run application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access API**
   - API Docs: http://localhost:8000/api/docs
   - ReDoc: http://localhost:8000/api/redoc
   - Health: http://localhost:8000/health

## 📚 API Endpoints

### Users
```
POST   /api/v1/users/                    Create user
GET    /api/v1/users/                    List users (superuser)
GET    /api/v1/users/{id}                Get user
GET    /api/v1/users/me                  Get current user
PUT    /api/v1/users/{id}                Update user
DELETE /api/v1/users/{id}                Delete user
POST   /api/v1/users/{id}/deactivate     Deactivate user
POST   /api/v1/users/{id}/activate       Activate user (superuser)
```

### Lists
```
POST   /api/v1/lists/                    Create list
GET    /api/v1/lists/                    Get user's lists
GET    /api/v1/lists/{id}                Get list with items
PUT    /api/v1/lists/{id}                Update list
DELETE /api/v1/lists/{id}                Delete list
POST   /api/v1/lists/{id}/archive        Archive list
POST   /api/v1/lists/{id}/unarchive      Unarchive list
```

### List Items
```
POST   /api/v1/lists/{list_id}/items                Create item
GET    /api/v1/lists/{list_id}/items                Get items
GET    /api/v1/lists/{list_id}/items/{id}          Get item
PUT    /api/v1/lists/{list_id}/items/{id}          Update item
DELETE /api/v1/lists/{list_id}/items/{id}          Delete item
POST   /api/v1/lists/{list_id}/items/{id}/toggle   Toggle completion
```

## 🔐 Authentication

### Flow
1. Client sends credentials to login endpoint
2. Server validates credentials and issues JWT token
3. Client includes token in Authorization header
4. Server validates token and returns user data

### Token Usage
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" http://localhost:8000/api/v1/users/me
```

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter  
- At least one digit

## 📊 Data Models

### User
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
```

### List
```python
- id (PK)
- title
- description
- owner_id (FK → users.id)
- is_archived
- created_at
- updated_at
```

### ListItem
```python
- id (PK)
- list_id (FK → lists.id)
- content
- is_completed
- order
- created_at
- updated_at
```

## 🗄️ Database Migrations

### Create Migration
```bash
alembic revision --autogenerate -m "Description"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback
```bash
alembic downgrade -1
```

### View History
```bash
alembic history
```

## 🧪 Testing

### Run Tests
```bash
pytest                           # All tests
pytest tests/test_users.py      # Specific file
pytest --cov=app                # With coverage
```

### Manual Testing
See [test_examples.py](test_examples.py) for curl examples and test cases.

## ⚙️ Configuration

### Environment Variables
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

# Rate Limiting
RATE_LIMIT_DEFAULT=100/minute
RATE_LIMIT_AUTH=30/minute

# Logging
LOG_LEVEL=INFO
```

### Settings
Edit [app/core/config.py](app/core/config.py) to customize:
- Rate limiting defaults
- CORS origins
- Token expiration
- Database connection

## 🚦 Rate Limiting

Default limits:
- General endpoints: 100 requests/minute
- Auth endpoints: 30 requests/minute

Rate limit exceeded returns HTTP 429.

## 🌐 CORS

Default allowed origins:
- http://localhost
- http://localhost:3000
- http://localhost:8000
- http://localhost:8080

Customize in `.env` or `config.py`.

## 📖 Documentation

### Included Documentation
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Comprehensive API reference
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Installation and setup guide
- [test_examples.py](test_examples.py) - Testing examples

### Auto-Generated Docs
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 🏗️ Architecture Patterns

### Repository Pattern
- Separates data access from business logic
- Enables easy testing with mock repositories
- Centralizes query logic

### Service Layer
- Contains business logic and validation
- Handles authorization checks
- Manages transactions

### Dependency Injection
- Clean endpoint handlers
- Testable dependencies
- Loose coupling

## 🔒 Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ CORS middleware
- ✅ Rate limiting
- ✅ Input validation
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ XSS protection (via Pydantic)
- ✅ Authorization checks

## 🐛 Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error type",
  "details": [
    {
      "field": "field_name",
      "message": "Error description"
    }
  ]
}
```

## 📈 Performance

### Optimizations
- Database indexes on frequently queried columns
- Pagination for large result sets
- Query optimization in repositories
- Connection pooling

### Scalability
- Stateless design - horizontal scaling ready
- Database-agnostic ORM (SQLAlchemy)
- Async/await support (uvicorn)
- Rate limiting for DOS protection

## 🚢 Deployment

### Docker
```bash
docker-compose up -d
```

### Cloud Deployment
See `deployment/` directory for:
- AWS Elastic Container Service (ECS)
- AWS Lambda
- AWS Elastic Beanstalk

### Pre-Deployment Checklist
- [ ] Update SECRET_KEY
- [ ] Configure DATABASE_URL
- [ ] Update CORS_ORIGINS
- [ ] Enable HTTPS
- [ ] Set LOG_LEVEL appropriately
- [ ] Configure monitoring
- [ ] Set up backups
- [ ] Security audit

## 📝 Example Usage

### Create User
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "SecurePass123"
  }'
```

### Create List
```bash
curl -X POST "http://localhost:8000/api/v1/lists/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Shopping",
    "description": "Weekly groceries"
  }'
```

### Add Item to List
```bash
curl -X POST "http://localhost:8000/api/v1/lists/1/items" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Buy milk",
    "is_completed": false
  }'
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Add tests
4. Update documentation
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 📞 Support

For issues and questions:
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- Review [SETUP_GUIDE.md](SETUP_GUIDE.md)
- See [test_examples.py](test_examples.py) for API examples
- Open an issue on GitHub

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [Alembic Tutorial](https://alembic.sqlalchemy.org)

## 🛣️ Roadmap

### Planned Features
- [ ] WebSocket support for real-time updates
- [ ] File attachments for items
- [ ] List sharing with other users
- [ ] Due dates and reminders
- [ ] Activity history/audit logs
- [ ] Advanced search and filtering
- [ ] Email notifications
- [ ] Two-factor authentication
- [ ] OAuth2 integration
- [ ] Analytics dashboard

---

**Created**: January 2024  
**Version**: 1.0.0  
**Status**: Production Ready ✨
