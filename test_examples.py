"""
API Testing Examples and Test Suite

This file contains examples for testing the FastAPI application
using Python requests or pytest.

Run with: pytest test_examples.py -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.core.config import settings
from app.models.user import User

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create test database tables"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestUserEndpoints:
    """Test user CRUD endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset database before each test"""
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    
    def test_create_user(self):
        """Test user creation"""
        response = client.post(
            "/api/v1/users/",
            json={
                "email": "testuser@example.com",
                "full_name": "Test User",
                "is_active": True
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "testuser@example.com"
        assert data["full_name"] == "Test User"
        assert "id" in data
    
    def test_create_user_duplicate_email(self):
        """Test creating user with duplicate email"""
        # Create first user
        client.post(
            "/api/v1/users/",
            json={
                "email": "duplicate@example.com",
                "full_name": "User One"
            }
        )
        
        # Try to create with same email
        response = client.post(
            "/api/v1/users/",
            json={
                "email": "duplicate@example.com",
                "full_name": "User Two"
            }
        )
        assert response.status_code == 409
    
    def test_create_user_invalid_email(self):
        """Test user creation with invalid email"""
        response = client.post(
            "/api/v1/users/",
            json={
                "email": "notanemail",
                "full_name": "Invalid Email"
            }
        )
        assert response.status_code == 422




class TestValidation:
    """Test input validation"""
    
    def test_email_validation(self):
        """Test email field validation"""
        response = client.post(
            "/api/v1/users/",
            json={
                "email": "@invalid.com",
                "full_name": "Invalid Email"
            }
        )
        assert response.status_code == 422
    
    def test_string_length_validation(self):
        """Test string length validation"""
        response = client.post(
            "/api/v1/users/",
            json={
                "email": "toolong@example.com",
                "full_name": "a" * 256  # Exceeds max length
            }
        )
        assert response.status_code == 422


# ============================================================================
# Manual API Testing Examples
# ============================================================================

"""
curl Examples for Manual Testing:

1. Create User:
   curl -X POST "http://localhost:8000/api/v1/users/" \\
     -H "Content-Type: application/json" \\
     -d '{
       "email": "newuser@example.com",
       "full_name": "New User",
       "is_active": true
     }'

2. Get All Users:
   curl -X GET "http://localhost:8000/api/v1/users/" \\
     -H "Content-Type: application/json"

3. Get User by ID:
   curl -X GET "http://localhost:8000/api/v1/users/1"

4. Update User:
   curl -X PUT "http://localhost:8000/api/v1/users/1" \\
     -H "Content-Type: application/json" \\
     -d '{
       "full_name": "Updated Name",
       "email": "newemail@example.com"
     }'

5. Create List:
   curl -X POST "http://localhost:8000/api/v1/lists/" \\
     -H "Content-Type: application/json" \\
     -H "Authorization: Bearer YOUR_TOKEN" \\
     -d '{
       "title": "Shopping List",
       "description": "Weekly groceries",
       "is_archived": false
     }'

6. Get User's Lists:
   curl -X GET "http://localhost:8000/api/v1/lists/?skip=0&limit=20" \\
     -H "Authorization: Bearer YOUR_TOKEN"

7. Add List Item:
   curl -X POST "http://localhost:8000/api/v1/lists/1/items" \\
     -H "Content-Type: application/json" \\
     -H "Authorization: Bearer YOUR_TOKEN" \\
     -d '{
       "content": "Buy milk",
       "is_completed": false,
       "order": 0
     }'

8. Toggle Item Completion:
   curl -X POST "http://localhost:8000/api/v1/lists/1/items/1/toggle" \\
     -H "Authorization: Bearer YOUR_TOKEN"

9. Delete User:
   curl -X DELETE "http://localhost:8000/api/v1/users/1"

10. Get Health Check:
    curl -X GET "http://localhost:8000/health"
"""
