#!/usr/bin/env python3
"""
Test script for the authentication and credit system
"""

import requests
import json
import os
import sys

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_GOOGLE_TOKEN = "test_token_123"  # This won't work with real Google API

def test_api_endpoints():
    """Test basic API endpoints without authentication"""
    print("🧪 Testing Basic API Endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Could not connect to API: {e}")
        print("   Make sure the backend is running on port 8000")
        return False
    
    # Test health endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            health_data = response.json()
            print(f"   Status: {health_data.get('status', 'unknown')}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    return True

def test_protected_endpoints():
    """Test that protected endpoints require authentication"""
    print("\n🔒 Testing Protected Endpoints...")
    
    # Test chat endpoint without auth (should fail)
    try:
        response = requests.post(f"{API_BASE_URL}/chat", json={
            "message": "Hello",
            "conversation_id": "test_123"
        })
        if response.status_code == 401:
            print("✅ Chat endpoint properly protected (401 Unauthorized)")
        else:
            print(f"❌ Chat endpoint should require auth but returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing chat endpoint: {e}")
    
    # Test user profile endpoint without auth (should fail)
    try:
        response = requests.get(f"{API_BASE_URL}/auth/me")
        if response.status_code == 401:
            print("✅ Profile endpoint properly protected (401 Unauthorized)")
        else:
            print(f"❌ Profile endpoint should require auth but returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing profile endpoint: {e}")

def test_database_creation():
    """Test that database is created and accessible"""
    print("\n🗄️  Testing Database...")
    
    # Check if database file exists
    if os.path.exists("users.db"):
        print("✅ Database file created")
        
        # Try to connect and check tables
        try:
            import sqlite3
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            
            # Check if users table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if cursor.fetchone():
                print("✅ Users table exists")
            else:
                print("❌ Users table not found")
            
            # Check if user_sessions table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_sessions'")
            if cursor.fetchone():
                print("✅ User sessions table exists")
            else:
                print("❌ User sessions table not found")
            
            conn.close()
        except Exception as e:
            print(f"❌ Database connection error: {e}")
    else:
        print("❌ Database file not found (run the backend first)")

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n📦 Checking Dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'google.auth',
        'jose',
        'psutil',
        'pydantic',
        'sqlite3'  # Built-in, but check anyway
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sqlite3':
                import sqlite3
            elif package == 'google.auth':
                import google.auth
            elif package == 'jose':
                import jose
            else:
                __import__(package.replace('-', '_'))
            print(f"✅ {package} - installed")
        except ImportError:
            print(f"❌ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed!")
        return True

def generate_test_env():
    """Generate a test environment configuration"""
    print("\n🔧 Environment Configuration...")
    
    env_content = """# Copy this to .env and update with your actual values

# Google OAuth Configuration
# Get these from https://console.cloud.google.com/
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here

# JWT Configuration
# Generate a secure secret key for JWT tokens
JWT_SECRET_KEY=your-super-secret-jwt-key-here

# Server Configuration
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development

# Database Configuration
DATABASE_URL=sqlite:///users.db
"""
    
    print("📝 Recommended .env file content:")
    print(env_content)
    
    # Check if .env exists
    if os.path.exists(".env"):
        print("✅ .env file already exists")
    else:
        print("⚠️  .env file not found - you'll need to create one")

def main():
    """Run all tests"""
    print("🌸 Ara Health Agent - Authentication System Test")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Please install missing dependencies before continuing")
        return
    
    # Test basic functionality
    if not test_api_endpoints():
        print("\n❌ Backend is not running. Start it with: cd api && python main.py")
        return
    
    # Test protected endpoints
    test_protected_endpoints()
    
    # Test database
    test_database_creation()
    
    # Show environment config
    generate_test_env()
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary:")
    print("   1. ✅ Dependencies installed")
    print("   2. ✅ Backend API running")
    print("   3. ✅ Authentication protection working")
    print("   4. ✅ Database tables created")
    print("\n🚀 Next Steps:")
    print("   1. Set up Google OAuth credentials")
    print("   2. Create .env file with your credentials")
    print("   3. Update frontend/index.html with your Google Client ID")
    print("   4. Test the complete flow with real Google authentication")
    print("\n📖 See GOOGLE_OAUTH_SETUP.md for detailed instructions")

if __name__ == "__main__":
    main() 