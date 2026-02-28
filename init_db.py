#!/usr/bin/env python
"""
Database initialization and seeding script

Usage:
    python init_db.py

This script:
1. Creates all database tables from models
2. Seeds initial test users (admin and regular user)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings
from app.db.base import Base
from app.models.user import User


def init_db():
    """Initialize database - create all tables"""
    print("🔄 Initializing database...")
    
    # Create engine
    engine = create_engine(settings.DATABASE_URL, echo=True)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    
    return engine


def seed_data(engine):
    """Seed initial test data"""
    print("\n📊 Seeding initial data...")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if user exists
        existing_user = session.query(User).filter_by(email="admin@example.com").first()
        if existing_user:
            print("⚠️  Admin user already exists, skipping seeding")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password="AUTH_DISABLED",
            is_active=True,
            is_superuser=True
        )
        session.add(admin_user)
        session.flush()
        
        print(f"✅ Created admin user: admin@example.com")
        
        # Create test user
        test_user = User(
            email="test@example.com",
            full_name="Test User",
            hashed_password="AUTH_DISABLED",
            is_active=True,
            is_superuser=False
        )
        session.add(test_user)
        session.flush()
        
        print(f"✅ Created test user: test@example.com")
        
        session.commit()
        print("\n✅ Database seeding completed successfully!")
        
        print("\n📋 Test Users:")
        print("  Admin User: admin@example.com")
        print("  Test User: test@example.com")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error seeding data: {str(e)}")
        raise
    finally:
        session.close()


def main():
    """Main initialization flow"""
    print("🚀 FastAPI Users API - Database Initialization\n")
    
    # Check if DATABASE_URL is set
    if not settings.DATABASE_URL:
        print("❌ DATABASE_URL not set in environment variables")
        print("Please set DATABASE_URL and try again")
        sys.exit(1)
    
    try:
        # Initialize database
        engine = init_db()
        
        # Seed data
        seed_data(engine)
        
        print("\n✨ Initialization complete! Ready to start the application.")
        print("\nNext steps:")
        print("1. Run: uvicorn app.main:app --reload")
        print("2. Visit: http://localhost:8000/api/docs")
        print("3. Use user CRUD endpoints from /api/docs")
        
    except Exception as e:
        print(f"\n❌ Initialization failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
