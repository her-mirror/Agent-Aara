from google.auth.transport import requests
from google.oauth2 import id_token
from jose import JWTError, jwt
from datetime import datetime, timedelta
import secrets
import sqlite3
import os
import logging
from typing import Optional, Dict, Any
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

# Database setup
DATABASE_FILE = "users.db"

security = HTTPBearer()

def init_database():
    """Initialize the user database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            google_id TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            picture TEXT,
            credits INTEGER DEFAULT 100,
            total_messages INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create user_sessions table for tracking active sessions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            conversation_id TEXT,
            messages_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

class UserManager:
    """Manage user operations and credit system"""
    
    @staticmethod
    def get_user_by_google_id(google_id: str) -> Optional[Dict[str, Any]]:
        """Get user by Google ID"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, google_id, email, name, picture, credits, total_messages, created_at, last_login
            FROM users WHERE google_id = ?
        ''', (google_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "google_id": row[1],
                "email": row[2],
                "name": row[3],
                "picture": row[4],
                "credits": row[5],
                "total_messages": row[6],
                "created_at": row[7],
                "last_login": row[8]
            }
        return None
    
    @staticmethod
    def create_user(google_id: str, email: str, name: str, picture: str = None) -> Dict[str, Any]:
        """Create a new user with 100 credits"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (google_id, email, name, picture, credits)
                VALUES (?, ?, ?, ?, 100)
            ''', (google_id, email, name, picture))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"New user created: {email} with 100 credits")
            
            return {
                "id": user_id,
                "google_id": google_id,
                "email": email,
                "name": name,
                "picture": picture,
                "credits": 100,
                "total_messages": 0,
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat()
            }
            
        except sqlite3.IntegrityError:
            conn.rollback()
            raise HTTPException(status_code=400, detail="User already exists")
        finally:
            conn.close()
    
    @staticmethod
    def update_last_login(user_id: int):
        """Update user's last login timestamp"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_user_credits(user_id: int) -> int:
        """Get user's current credits"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT credits FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else 0
    
    @staticmethod
    def deduct_credit(user_id: int) -> bool:
        """Deduct 1 credit from user. Returns True if successful, False if insufficient credits"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Check current credits
        cursor.execute('SELECT credits FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        
        if not row or row[0] <= 0:
            conn.close()
            return False
        
        # Deduct credit and increment message count
        cursor.execute('''
            UPDATE users 
            SET credits = credits - 1, total_messages = total_messages + 1 
            WHERE id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Credit deducted for user {user_id}. Remaining credits: {row[0] - 1}")
        return True
    
    @staticmethod
    def add_credits(user_id: int, amount: int) -> bool:
        """Add credits to user (for admin use or purchases)"""
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET credits = credits + ? WHERE id = ?
        ''', (amount, user_id))
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        if affected_rows > 0:
            logger.info(f"Added {amount} credits to user {user_id}")
            return True
        return False

class GoogleAuth:
    """Handle Google OAuth authentication"""
    
    @staticmethod
    def verify_google_token(token: str) -> Dict[str, Any]:
        """Verify Google ID token and return user info"""
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), GOOGLE_CLIENT_ID
            )
            
            # Verify issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            return {
                "google_id": idinfo['sub'],
                "email": idinfo['email'],
                "name": idinfo.get('name', ''),
                "picture": idinfo.get('picture', ''),
                "email_verified": idinfo.get('email_verified', False)
            }
            
        except ValueError as e:
            logger.error(f"Invalid Google token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Verify JWT token and return user info"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        # Get user from database
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, google_id, email, name, picture, credits, total_messages
            FROM users WHERE id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return {
            "id": row[0],
            "google_id": row[1],
            "email": row[2],
            "name": row[3],
            "picture": row[4],
            "credits": row[5],
            "total_messages": row[6]
        }
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

def get_current_user(user: Dict[str, Any] = Depends(verify_token)) -> Dict[str, Any]:
    """Get current authenticated user"""
    return user

def require_credits(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require user to have at least 1 credit"""
    if user["credits"] <= 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient credits. Please purchase more credits to continue."
        )
    return user

# Initialize database when module is imported
init_database() 