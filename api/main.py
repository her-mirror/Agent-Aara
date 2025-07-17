from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import sys
import os
import uvicorn

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.agent.workflow import run_workflow
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

app = FastAPI(
    title="Ara Health Agent API",
    description="AI-powered women's health and skincare assistant",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-nextjs-domain.com"],  # Update with your Next.js domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed error messages"""
    print(f"Validation error: {exc}")
    print(f"Request body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "message": "Request validation failed",
            "body": await request.body() if hasattr(request, 'body') else None
        }
    )

# Request/Response models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    chat_history: Optional[List[Dict[str, Any]]] = []  # More flexible - accept any dict format

class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None
    status: str = "success"
    metadata: Optional[Dict[str, Any]] = {}

class HealthStatus(BaseModel):
    status: str
    version: str
    components: Dict[str, str]

# In-memory storage for conversations (in production, use a proper database)
conversations: Dict[str, List[Dict[str, str]]] = {}

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Ara Health Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.post("/test-chat")
async def test_chat(data: Dict[str, Any]):
    """Test endpoint to debug request format"""
    try:
        print(f"Received test data: {data}")
        return {
            "received": data,
            "status": "success",
            "message": "Data received successfully"
        }
    except Exception as e:
        print(f"Test endpoint error: {e}")
        return {
            "error": str(e),
            "status": "error"
        }

@app.post("/debug-chat-history")
async def debug_chat_history(request: ChatRequest):
    """Debug endpoint to test chat history parsing"""
    print(f"\n🔍 DEBUG CHAT HISTORY:")
    print(f"📨 Full request: {request}")
    print(f"📨 Request dict: {request.dict()}")
    
    if request.chat_history:
        for i, msg in enumerate(request.chat_history):
            print(f"\n📨 Message {i+1}:")
            print(f"  Type: {type(msg)}")
            print(f"  Value: {msg}")
            print(f"  Dict representation: {dict(msg) if hasattr(msg, '__dict__') else 'N/A'}")
    
    return {
        "message": request.message,
        "conversation_id": request.conversation_id,
        "chat_history_count": len(request.chat_history) if request.chat_history else 0,
        "chat_history": request.chat_history,
        "status": "debug_complete"
    }

@app.get("/health", response_model=HealthStatus)
async def health_check():
    """Health check endpoint"""
    return HealthStatus(
        status="healthy",
        version="1.0.0",
        components={
            "workflow": "operational",
            "rules_engine": "operational",
            "tools": "operational"
        }
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        print(f"\n🔍 FULL REQUEST DEBUG:")
        print(f"📨 Message: '{request.message}'")
        print(f"📨 Conversation ID: '{request.conversation_id}'")
        print(f"📨 Chat History Type: {type(request.chat_history)}")
        print(f"📨 Chat History Length: {len(request.chat_history) if request.chat_history else 0}")
        # Convert chat history to the format expected by the workflow
        chat_history = []
        if request.chat_history:
            print(f"\n📨 INCOMING CHAT HISTORY: {len(request.chat_history)} messages")
            print(f"📨 RAW CHAT HISTORY: {request.chat_history}")
            
            for i, msg in enumerate(request.chat_history):
                print(f"\n📨 Message {i+1}: {msg}")
                print(f"📨 Message type: {type(msg)}")
                
                # Handle multiple formats
                if isinstance(msg, dict):
                    # Support multiple formats:
                    # Format 1: {"role": "user", "content": "text"}
                    # Format 2: {"from": "user", "text": "text"} 
                    role = ""
                    content = ""
                    
                    if "role" in msg:
                        role = msg["role"] or ""
                    elif "from" in msg:
                        role = msg["from"] or ""
                    
                    if "content" in msg:
                        content = msg["content"] or ""
                    elif "text" in msg:
                        content = msg["text"] or ""
                    
                    print(f"📨 Dict format - role: '{role}', content: '{content[:50]}...'")
                else:
                    role = ""
                    content = ""
                    
                    if hasattr(msg, "role") and msg.role:
                        role = str(msg.role)
                    elif hasattr(msg, "from") and msg.from_:
                        role = str(msg.from_)
                    
                    if hasattr(msg, "content") and msg.content:
                        content = str(msg.content)
                    elif hasattr(msg, "text") and msg.text:
                        content = str(msg.text)
                    
                    print(f"📨 Object format - role: '{role}', content: '{content[:50]}...'")
                
                # Normalize role names
                if role.lower() in ["user", "human"]:
                    role = "user"
                elif role.lower() in ["assistant", "aara", "ara", "bot", "ai"]:
                    role = "assistant"
                
                print(f"  - {role}: {content[:50]}...")
                
                if role == "user":
                    chat_history.append({"user": content, "ara": ""})
                    print(f"✅ Added user message to chat_history")
                elif role == "assistant" and chat_history:
                    chat_history[-1]["ara"] = content
                    print(f"✅ Added assistant response to last exchange")
                elif role == "assistant" and not chat_history:
                    # First message is assistant - create empty user entry
                    chat_history.append({"user": "", "ara": content})
                    print(f"✅ Added assistant-first message to chat_history")
                else:
                    print(f"❌ Skipped message - role: '{role}', has_previous_exchange: {len(chat_history) > 0}")
        
        print(f"\n📤 CONVERTED CHAT HISTORY FOR WORKFLOW: {len(chat_history)} exchanges")
        for i, exchange in enumerate(chat_history[-2:]):  # Show last 2 exchanges
            print(f"  {i+1}. User: {exchange.get('user', '')[:40]}...")
            print(f"     Ara: {exchange.get('ara', '')[:40]}...")
        
        # Run the workflow
        response = run_workflow(request.message, chat_history)
        
        # Store conversation if conversation_id is provided
        if request.conversation_id:
            if request.conversation_id not in conversations:
                conversations[request.conversation_id] = []
            conversations[request.conversation_id].append({
                "user": request.message,
                "ara": response
            })
        
        return ChatResponse(
            response=response,
            conversation_id=request.conversation_id,
            status="success",
            metadata={
                "message_length": len(response),
                "conversation_length": len(conversations.get(request.conversation_id, []))
            }
        )
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        print(f"Request data: {request}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conversation_id,
        "messages": conversations[conversation_id]
    }

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    del conversations[conversation_id]
    return {"message": "Conversation deleted successfully"}

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint (for future implementation)"""
    # Placeholder for streaming functionality
    response = await chat(request)
    return response

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    default_port = int(os.environ.get("PORT", "8000"))
    parser.add_argument("--port", type=int, default=default_port, help="Port to run the server on")
    args = parser.parse_args()
    
    # Use environment variables for production deployment
    port = int(os.environ.get("PORT", str(args.port)))
    host = os.environ.get("HOST", "0.0.0.0")
    reload_mode = os.environ.get("ENVIRONMENT", "development") == "development"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload_mode,
        log_level="info"
    ) 