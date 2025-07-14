from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

# Request/Response models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    chat_history: Optional[List[ChatMessage]] = []

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
        # Convert chat history to the format expected by the workflow
        chat_history = []
        if request.chat_history:
            for msg in request.chat_history:
                if msg.role == "user":
                    chat_history.append({"user": msg.content, "ara": ""})
                elif msg.role == "assistant" and chat_history:
                    chat_history[-1]["ara"] = msg.content
        
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
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=args.port,
        reload=True,
        log_level="info"
    ) 