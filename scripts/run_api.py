#!/usr/bin/env python3
"""
Script to run the Ara Health Agent API server
"""
import os
import sys
import uvicorn

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def main():
    """Start the FastAPI server"""
    print("🌸 Starting Ara Health Agent API Server...")
    print("📡 API Documentation: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    print("💬 Chat Endpoint: http://localhost:8000/chat")
    print("-" * 50)
    
    try:
        # Import and run the API
        from api.main import app
        
        uvicorn.run(
            "api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🌸 Ara API Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting API server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 