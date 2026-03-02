# Quick Start - Users Only API

## ✅ What's Been Done

1. ✅ Fixed async driver issue (psycopg2 → sync SQLAlchemy)
2. ✅ Converted all endpoints to synchronous
3. ✅ Updated database migrations (users table only)
4. ✅ Cleaned requirements.txt
5. ✅ Removed list service/repository imports

## 🚀 Get Started in 5 Minutes

### Step 1: Install & Setup
```bash
# Fresh install of dependencies
pip install --upgrade -r requirements.txt

# Initialize database
python init_db.py
```

### Step 2: Run the Server
```bash
uvicorn app.main:app --reload
```

### Step 3: Test It Works
```bash
# Health check
curl http://localhost:8000/health

# Create a user
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"TestPass123"}'
```

### Step 4: View API Docs
Open: http://localhost:8000/api/docs

## 📦 Optional: Clean Up Unused Files

These files are for List functionality that's no longer used:

```bash
# Remove these files:
rm app/models/list.py
rm app/repositories/list_repository.py  
rm app/services/list_service.py
rm app/api/v1/endpoints/lists.py
rm app/schemas/v1/list.py
```

## 🔑 Test Credentials (from init_db.py)

```
Admin User:
  Email: admin@example.com
  Password: AdminPass123
  
Test User:
  Email: test@example.com
  Password: TestPass123
```

## 📝 Available User Endpoints

```
POST   /api/v1/users/               Create user
GET    /api/v1/users/               List users (admin only)
GET    /api/v1/users/me             Get current user
GET    /api/v1/users/{id}           Get user by ID
PUT    /api/v1/users/{id}           Update user
DELETE /api/v1/users/{id}           Delete user
POST   /api/v1/users/{id}/deactivate   Deactivate user
POST   /api/v1/users/{id}/activate     Activate user (admin)
```

## ⚙️ Configuration

Edit `.env` if needed:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_db
SECRET_KEY=your-secret-key
LOG_LEVEL=INFO
```

## 🐛 Troubleshooting

### "Module not found" errors
```bash
# Clear cache and reinstall
rm -rf __pycache__ .pytest_cache
pip install --force-reinstall -r requirements.txt
```

### Database connection errors
```bash
# Check PostgreSQL is running and database exists
# Update DATABASE_URL in .env
alembic upgrade head
```

### Port already in use
```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

## 📚 Full Documentation

- **API Reference**: `API_QUICK_REFERENCE.md`
- **Setup Guide**: `SETUP_GUIDE.md`
- **Changelog**: `USERS_ONLY_CHANGELOG.md`
- **Full Docs**: `API_DOCUMENTATION.md`

## ✨ Architecture Highlights

- **Pattern**: Repository → Service → Endpoint
- **Validation**: Pydantic schemas with custom validators
- **Auth**: JWT + bcrypt password hashing
- **Rate Limiting**: slowapi middleware (100 req/min)
- **CORS**: Configurable origins
- **Migrations**: Alembic for database versioning

---

**Ready to Code!** 🚀  
Start the server and visit `/api/docs` for interactive API testing.
