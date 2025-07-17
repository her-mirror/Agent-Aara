#!/usr/bin/env python3
import os
import sys
import uvicorn

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    # Get port from environment (Render provides this)
    port = int(os.environ.get("PORT", 8000))
    
    # Set production environment
    os.environ.setdefault("ENVIRONMENT", "production")
    
    print(f"🚀 Starting Ara Health Agent API on port {port}")
    print(f"Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    
    # Initialize vector store if needed
    print("📚 Initializing vector store...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, "scripts/setup_vectorstore.py"], 
                              capture_output=True, text=True, cwd=project_root)
        if result.returncode == 0:
            print("✅ Vector store initialized successfully")
        else:
            print(f"⚠️ Vector store setup warning: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Vector store initialization failed: {e}")
        print("Continuing without vector store...")
    
    # Import here to ensure path is set
    try:
        from api.main import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
    except ImportError as e:
        print(f"Import error: {e}")
        print("Current working directory:", os.getcwd())
        print("Python path:", sys.path)
        sys.exit(1)

if __name__ == "__main__":
    main() 