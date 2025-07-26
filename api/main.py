# from fastapi import FastAPI, HTTPException, Request, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from typing import List, Dict, Any, Optional
# import sys
# import os
# import uvicorn
# import psutil
# import time
# import logging
# import asyncio
# import json
# from datetime import datetime
# from fastapi.responses import StreamingResponse

# # Add project root to Python path
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# try:
#     from src.agent.workflow import run_workflow
#     # from auth import (
#     #     GoogleAuth, UserManager, create_access_token, 
#     #     get_current_user, require_credits, verify_token
#     # )
# except ImportError as e:
#     print(f"Import error: {e}")
#     print("Make sure all dependencies are installed: pip install -r requirements.txt")
#     sys.exit(1)

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# app = FastAPI(
#     title="Aara Health Agent API",
#     description="AI-powered women's health and skincare assistant",
#     version="1.0.0"
# )

# # System monitoring functions
# def get_system_metrics():
#     """Get current system resource usage"""
#     try:
#         cpu_percent = psutil.cpu_percent(interval=0.1)
#         memory = psutil.virtual_memory()
#         memory_used_mb = memory.used / (1024 * 1024)
#         memory_total_mb = memory.total / (1024 * 1024)
#         memory_percent = memory.percent
        
#         process = psutil.Process()
#         process_memory = process.memory_info()
#         process_memory_mb = process_memory.rss / (1024 * 1024)
#         process_cpu_percent = process.cpu_percent()
        
#         return {
#             "timestamp": datetime.now().isoformat(),
#             "system_cpu_percent": round(cpu_percent, 2),
#             "system_memory_used_mb": round(memory_used_mb, 2),
#             "system_memory_total_mb": round(memory_total_mb, 2),
#             "system_memory_percent": round(memory_percent, 2),
#             "process_memory_mb": round(process_memory_mb, 2),
#             "process_cpu_percent": round(process_cpu_percent, 2)
#         }
#     except Exception as e:
#         logger.error(f"Error getting system metrics: {e}")
#         return {
#             "timestamp": datetime.now().isoformat(),
#             "system_cpu_percent": 0,
#             "system_memory_used_mb": 0,
#             "system_memory_total_mb": 0,
#             "system_memory_percent": 0,
#             "process_memory_mb": 0,
#             "process_cpu_percent": 0,
#             "error": str(e)
#         }

# class ChatMetricsTracker:
#     """Track detailed metrics for individual chat sessions"""
    
#     def __init__(self, conversation_id: str, message: str):
#         self.conversation_id = conversation_id
#         self.message = message
#         self.start_time = time.time()
#         self.metrics_history = []
#         self.peak_metrics = {
#             "cpu": 0,
#             "memory": 0
#         }
#         self.low_metrics = {
#             "cpu": float('inf'),
#             "memory": float('inf')
#         }
    
#     def capture_metrics(self, stage: str):
#         """Capture metrics at different stages"""
#         metrics = get_system_metrics()
#         metrics["stage"] = stage
#         metrics["elapsed_ms"] = round((time.time() - self.start_time) * 1000, 2)
        
#         cpu = metrics.get("system_cpu_percent", 0)
#         memory = metrics.get("process_memory_mb", 0)
        
#         if cpu > self.peak_metrics["cpu"]:
#             self.peak_metrics["cpu"] = cpu
#         if memory > self.peak_metrics["memory"]:
#             self.peak_metrics["memory"] = memory
            
#         if cpu < self.low_metrics["cpu"]:
#             self.low_metrics["cpu"] = cpu
#         if memory < self.low_metrics["memory"]:
#             self.low_metrics["memory"] = memory
        
#         self.metrics_history.append(metrics)
#         return metrics
    
#     def get_summary(self):
#         """Get complete summary of metrics for this chat"""
#         total_duration = round((time.time() - self.start_time) * 1000, 2)
        
#         return {
#             "conversation_id": self.conversation_id,
#             "message": self.message,
#             "total_duration_ms": total_duration,
#             "stages_count": len(self.metrics_history),
#             "peak_metrics": self.peak_metrics,
#             "low_metrics": self.low_metrics,
#             "metrics_history": self.metrics_history,
#             "summary": {
#                 "cpu_range": f"{self.low_metrics['cpu']}% - {self.peak_metrics['cpu']}%",
#                 "memory_range": f"{self.low_metrics['memory']:.1f}MB - {self.peak_metrics['memory']:.1f}MB",
#                 "performance_rating": "Good" if self.peak_metrics['cpu'] < 70 and self.peak_metrics['memory'] < 500 else "High Usage"
#             }
#         }

# # Live monitoring storage
# live_monitoring_clients = set()

# async def live_metrics_generator():
#     """Generate live metrics for SSE"""
#     while True:
#         try:
#             metrics = get_system_metrics()
#             yield f"data: {json.dumps(metrics)}\n\n"
#             await asyncio.sleep(1)  # Send metrics every second
#         except Exception as e:
#             yield f"data: {json.dumps({'error': str(e)})}\n\n"
#             await asyncio.sleep(5)

# # Middleware for monitoring requests
# @app.middleware("http")
# async def monitor_requests(request: Request, call_next):
#     """Monitor CPU and RAM usage for each request"""
#     start_time = time.time()
    
#     # Process the request
#     response = await call_next(request)
    
#     # Add basic metrics to response headers
#     processing_time = round((time.time() - start_time) * 1000, 2)
#     metrics = get_system_metrics()
    
#     response.headers["X-Processing-Time"] = str(processing_time)
#     response.headers["X-Memory-Usage"] = str(metrics.get('process_memory_mb', 0))
#     response.headers["X-CPU-Usage"] = str(metrics.get('system_cpu_percent', 0))
    
#     return response

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "https://your-nextjs-domain.com"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Add validation error handler
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     """Handle validation errors with detailed error messages"""
#     logger.error(f"Validation error: {exc}")
#     return JSONResponse(
#         status_code=422,
#         content={
#             "detail": exc.errors(),
#             "message": "Request validation failed"
#         }
#     )

# # Request/Response models
# class ChatMessage(BaseModel):
#     role: str  # "user" or "assistant"
#     content: str
#     timestamp: Optional[str] = None

# class ChatRequest(BaseModel):
#     message: str
#     conversation_id: Optional[str] = None
#     chat_history: Optional[List[Dict[str, Any]]] = []

# class ChatResponse(BaseModel):
#     response: str
#     conversation_id: Optional[str] = None
#     status: str = "success"
#     metadata: Optional[Dict[str, Any]] = {}

# class HealthStatus(BaseModel):
#     status: str
#     version: str
#     components: Dict[str, str]

# # Authentication models
# class GoogleSignInRequest(BaseModel):
#     google_token: str

# class AuthResponse(BaseModel):
#     access_token: str
#     token_type: str = "bearer"
#     user: Dict[str, Any]

# class UserProfile(BaseModel):
#     id: int
#     email: str
#     name: str
#     picture: Optional[str] = None
#     credits: int
#     total_messages: int

# class AddCreditsRequest(BaseModel):
#     user_id: int
#     amount: int

# # In-memory storage for conversations and metrics
# conversations: Dict[str, List[Dict[str, str]]] = {}
# conversation_metrics: Dict[str, List[Dict[str, Any]]] = {}

# @app.get("/")
# async def root():
#     """Root endpoint with API information"""
#     return {
#         "message": "Aara Health Agent API",
#         "version": "1.0.0",
#         "docs": "/docs",
#         "health": "/health",
#         "auth_required": True
#     }

# # Authentication endpoints
# @app.post("/auth/google", response_model=AuthResponse)
# async def google_sign_in(request: GoogleSignInRequest):
#     """Authenticate user with Google OAuth token"""
#     try:
#         # Verify Google token
#         google_user = GoogleAuth.verify_google_token(request.google_token)
        
#         # Check if user exists
#         user = UserManager.get_user_by_google_id(google_user["google_id"])
        
#         if not user:
#             # Create new user with 100 credits
#             user = UserManager.create_user(
#                 google_id=google_user["google_id"],
#                 email=google_user["email"],
#                 name=google_user["name"],
#                 picture=google_user.get("picture")
#             )
#             logger.info(f"New user registered: {user['email']}")
#         else:
#             # Update last login
#             UserManager.update_last_login(user["id"])
#             logger.info(f"User logged in: {user['email']}")
        
#         # Create access token
#         access_token = create_access_token(data={"user_id": user["id"]})
        
#         return AuthResponse(
#             access_token=access_token,
#             user={
#                 "id": user["id"],
#                 "email": user["email"],
#                 "name": user["name"],
#                 "picture": user.get("picture"),
#                 "credits": user["credits"],
#                 "total_messages": user["total_messages"]
#             }
#         )
        
#     except Exception as e:
#         logger.error(f"Authentication error: {e}")
#         raise HTTPException(
#             status_code=400,
#             detail=f"Authentication failed: {str(e)}"
#         )

# @app.get("/auth/me", response_model=UserProfile)
# async def get_current_user_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
#     """Get current user profile"""
#     return UserProfile(
#         id=current_user["id"],
#         email=current_user["email"],
#         name=current_user["name"],
#         picture=current_user.get("picture"),
#         credits=current_user["credits"],
#         total_messages=current_user["total_messages"]
#     )

# @app.get("/auth/credits")
# async def get_user_credits(current_user: Dict[str, Any] = Depends(get_current_user)):
#     """Get user's current credits"""
#     credits = UserManager.get_user_credits(current_user["id"])
#     return {
#         "user_id": current_user["id"],
#         "credits": credits,
#         "email": current_user["email"]
#     }

# @app.post("/admin/add-credits")
# async def add_credits_to_user(
#     request: AddCreditsRequest,
#     current_user: Dict[str, Any] = Depends(get_current_user)
# ):
#     """Add credits to a user (admin endpoint - in production, add proper admin auth)"""
#     # In production, add proper admin role checking here
#     success = UserManager.add_credits(request.user_id, request.amount)
    
#     if success:
#         return {
#             "message": f"Successfully added {request.amount} credits",
#             "user_id": request.user_id,
#             "status": "success"
#         }
#     else:
#         raise HTTPException(status_code=404, detail="User not found")

# @app.post("/test-chat")
# async def test_chat(data: Dict[str, Any]):
#     """Test endpoint to debug request format"""
#     try:
#         return {
#             "received": data,
#             "status": "success",
#             "message": "Data received successfully"
#         }
#     except Exception as e:
#         logger.error(f"Test endpoint error: {e}")
#         return {
#             "error": str(e),
#             "status": "error"
#         }

# @app.post("/debug-chat-history")
# async def debug_chat_history(request: ChatRequest):
#     """Debug endpoint to test chat history parsing"""
#     logger.info(f"Debug chat history: {len(request.chat_history) if request.chat_history else 0} messages")
    
#     return {
#         "message": request.message,
#         "conversation_id": request.conversation_id,
#         "chat_history_count": len(request.chat_history) if request.chat_history else 0,
#         "chat_history": request.chat_history,
#         "status": "debug_complete"
#     }

# @app.get("/health", response_model=HealthStatus)
# async def health_check():
#     """Health check endpoint with system metrics"""
#     metrics = get_system_metrics()
#     logger.info("Health check completed")
    
#     return HealthStatus(
#         status="healthy",
#         version="1.0.0",
#         components={
#             "workflow": "operational",
#             "rules_engine": "operational",
#             "tools": "operational",
#             "system_metrics": metrics
#         }
#     )

# @app.post("/chat", response_model=ChatResponse)
# async def chat(
#     request: ChatRequest, 
#     current_user: Dict[str, Any] = Depends(require_credits)
# ):
#     """Main chat endpoint with individual chat metrics tracking and credit system"""
    
#     # Check and deduct credit before processing
#     if not UserManager.deduct_credit(current_user["id"]):
#         raise HTTPException(
#             status_code=402,
#             detail="Insufficient credits. Please purchase more credits to continue."
#         )
    
#     conversation_id = request.conversation_id or f"chat_{current_user['id']}_{int(time.time())}"
#     tracker = ChatMetricsTracker(conversation_id, request.message)
    
#     try:
#         tracker.capture_metrics("request_received")
        
#         # Convert chat history to the format expected by the workflow
#         chat_history = []
#         if request.chat_history:
#             for msg in request.chat_history:
#                 role = ""
#                 content = ""
                
#                 if isinstance(msg, dict):
#                     if "role" in msg:
#                         role = msg["role"] or ""
#                     elif "from" in msg:
#                         role = msg["from"] or ""
                    
#                     if "content" in msg:
#                         content = msg["content"] or ""
#                     elif "text" in msg:
#                         content = msg["text"] or ""
#                 else:
#                     if hasattr(msg, "role") and msg.role:
#                         role = str(msg.role)
#                     elif hasattr(msg, "from") and msg.from_:
#                         role = str(msg.from_)
                    
#                     if hasattr(msg, "content") and msg.content:
#                         content = str(msg.content)
#                     elif hasattr(msg, "text") and msg.text:
#                         content = str(msg.text)
                
#                 # Normalize role names
#                 if role.lower() in ["user", "human"]:
#                     role = "user"
#                 elif role.lower() in ["assistant", "aAara", "Aara", "bot", "ai"]:
#                     role = "assistant"
                
#                 if role == "user":
#                     chat_history.append({"user": content, "Aara": ""})
#                 elif role == "assistant" and chat_history:
#                     chat_history[-1]["Aara"] = content
#                 elif role == "assistant" and not chat_history:
#                     chat_history.append({"user": "", "Aara": content})
        
#         tracker.capture_metrics("workflow_start")
#         logger.info(f"Processing chat for conversation: {conversation_id}")
        
#         response = run_workflow(request.message, chat_history)
        
#         tracker.capture_metrics("workflow_completed")
        
#         # Store conversation
#         if conversation_id not in conversations:
#             conversations[conversation_id] = []
#         conversations[conversation_id].append({
#             "user": request.message,
#             "Aara": response
#         })
        
#         # Store metrics
#         if conversation_id not in conversation_metrics:
#             conversation_metrics[conversation_id] = []
        
#         metrics_summary = tracker.get_summary()
#         conversation_metrics[conversation_id].append(metrics_summary)
        
#         # Get updated user credits
#         updated_credits = UserManager.get_user_credits(current_user["id"])
        
#         logger.info(f"Chat completed - Duration: {metrics_summary['total_duration_ms']}ms, Performance: {metrics_summary['summary']['performance_rating']}, Credits remaining: {updated_credits}")
        
#         return ChatResponse(
#             response=response,
#             conversation_id=conversation_id,
#             status="success",
#             metadata={
#                 "message_length": len(response),
#                 "conversation_length": len(conversations.get(conversation_id, [])),
#                 "user_credits_remaining": updated_credits,
#                 "credit_deducted": 1,
#                 "user_id": current_user["id"],
#                 "individual_chat_metrics": metrics_summary,
#                 "performance_summary": {
#                     "total_duration_ms": metrics_summary['total_duration_ms'],
#                     "peak_cpu_percent": metrics_summary['peak_metrics']['cpu'],
#                     "peak_memory_mb": metrics_summary['peak_metrics']['memory'],
#                     "low_cpu_percent": metrics_summary['low_metrics']['cpu'],
#                     "low_memory_mb": metrics_summary['low_metrics']['memory'],
#                     "performance_rating": metrics_summary['summary']['performance_rating'],
#                     "stages_tracked": metrics_summary['stages_count']
#                 }
#             }
#         )
    
#     except Exception as e:
#         logger.error(f"Error in chat endpoint: {e}")
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# @app.get("/live-metrics")
# async def live_metrics():
#     """Live system metrics stream using Server-Sent Events"""
#     return StreamingResponse(
#         live_metrics_generator(),
#         media_type="text/event-stream",
#         headers={
#             "Cache-Control": "no-cache",
#             "Connection": "keep-alive",
#             "Access-Control-Allow-Origin": "*",
#             "Access-Control-Allow-Headers": "Cache-Control"
#         }
#     )

# @app.get("/system-metrics")
# async def get_system_metrics_endpoint():
#     """Get current system resource usage metrics"""
#     metrics = get_system_metrics()
#     logger.info("System metrics requested")
    
#     return {
#         "timestamp": time.time(),
#         "metrics": metrics,
#         "status": "success"
#     }

# @app.get("/conversation-metrics/{conversation_id}")
# async def get_conversation_metrics(conversation_id: str):
#     """Get detailed metrics for a specific conversation"""
#     if conversation_id not in conversation_metrics:
#         raise HTTPException(status_code=404, detail="Conversation metrics not found")
    
#     metrics = conversation_metrics[conversation_id]
    
#     total_chats = len(metrics)
#     total_duration = sum(m['total_duration_ms'] for m in metrics)
#     avg_duration = total_duration / total_chats if total_chats > 0 else 0
    
#     peak_cpu_overall = max(m['peak_metrics']['cpu'] for m in metrics) if metrics else 0
#     peak_memory_overall = max(m['peak_metrics']['memory'] for m in metrics) if metrics else 0
    
#     logger.info(f"Conversation metrics requested for: {conversation_id}")
    
#     return {
#         "conversation_id": conversation_id,
#         "total_chats": total_chats,
#         "aggregate_stats": {
#             "total_duration_ms": total_duration,
#             "average_duration_ms": round(avg_duration, 2),
#             "peak_cpu_overall": peak_cpu_overall,
#             "peak_memory_overall": round(peak_memory_overall, 2)
#         },
#         "individual_chats": metrics,
#         "status": "success"
#     }

# @app.get("/all-conversation-metrics")
# async def get_all_conversation_metrics():
#     """Get metrics summary for all conversations"""
#     if not conversation_metrics:
#         return {
#             "total_conversations": 0,
#             "conversations": [],
#             "status": "success"
#         }
    
#     conversation_summaries = []
    
#     for conv_id, metrics in conversation_metrics.items():
#         total_chats = len(metrics)
#         total_duration = sum(m['total_duration_ms'] for m in metrics)
#         avg_duration = total_duration / total_chats if total_chats > 0 else 0
#         peak_cpu = max(m['peak_metrics']['cpu'] for m in metrics) if metrics else 0
#         peak_memory = max(m['peak_metrics']['memory'] for m in metrics) if metrics else 0
        
#         conversation_summaries.append({
#             "conversation_id": conv_id,
#             "total_chats": total_chats,
#             "total_duration_ms": total_duration,
#             "average_duration_ms": round(avg_duration, 2),
#             "peak_cpu_percent": peak_cpu,
#             "peak_memory_mb": round(peak_memory, 2),
#             "last_chat_time": metrics[-1]['metrics_history'][-1]['timestamp'] if metrics else None
#         })
    
#     conversation_summaries.sort(key=lambda x: x.get('last_chat_time', ''), reverse=True)
    
#     logger.info(f"All conversation metrics requested - {len(conversation_summaries)} conversations")
    
#     return {
#         "total_conversations": len(conversation_summaries),
#         "total_individual_chats": sum(s['total_chats'] for s in conversation_summaries),
#         "conversations": conversation_summaries,
#         "status": "success"
#     }

# @app.get("/conversations/{conversation_id}")
# async def get_conversation(conversation_id: str):
#     """Get conversation history"""
#     if conversation_id not in conversations:
#         raise HTTPException(status_code=404, detail="Conversation not found")
    
#     return {
#         "conversation_id": conversation_id,
#         "messages": conversations[conversation_id]
#     }

# @app.delete("/conversations/{conversation_id}")
# async def delete_conversation(conversation_id: str):
#     """Delete a conversation"""
#     if conversation_id not in conversations:
#         raise HTTPException(status_code=404, detail="Conversation not found")
    
#     del conversations[conversation_id]
#     return {"message": "Conversation deleted successfully"}

# @app.post("/chat/stream")
# async def chat_stream(request: ChatRequest):
#     """Streaming chat endpoint (for future implementation)"""
#     response = await chat(request)
#     return response

# if __name__ == "__main__":
#     import argparse
#     parser = argparse.ArgumentParser()
#     default_port = int(os.environ.get("PORT", "8000"))
#     parser.add_argument("--port", type=int, default=default_port, help="Port to run the server on")
#     args = parser.parse_args()
    
#     port = int(os.environ.get("PORT", str(args.port)))
#     host = os.environ.get("HOST", "0.0.0.0")
#     reload_mode = os.environ.get("ENVIRONMENT", "development") == "development"
    
#     uvicorn.run(
#         "main:app",
#         host=host,
#         port=port,
#         reload=reload_mode,
#         log_level="info"
#     ) 
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
    title="Aara Health Agent API",
    description="AI-powered women's health and skincare assistant",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://www.hermirror.life"],  # Update with your Next.js domain
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
        "message": "Aara Health Agent API",
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
                elif role.lower() in ["assistant", "aAara", "Aara", "bot", "ai"]:
                    role = "assistant"
                
                print(f"  - {role}: {content[:50]}...")
                
                if role == "user":
                    chat_history.append({"user": content, "Aara": ""})
                    print(f"✅ Added user message to chat_history")
                elif role == "assistant" and chat_history:
                    chat_history[-1]["Aara"] = content
                    print(f"✅ Added assistant response to last exchange")
                elif role == "assistant" and not chat_history:
                    # First message is assistant - create empty user entry
                    chat_history.append({"user": "", "Aara": content})
                    print(f"✅ Added assistant-first message to chat_history")
                else:
                    print(f"❌ Skipped message - role: '{role}', has_previous_exchange: {len(chat_history) > 0}")
        
        print(f"\n📤 CONVERTED CHAT HISTORY FOR WORKFLOW: {len(chat_history)} exchanges")
        for i, exchange in enumerate(chat_history[-2:]):  # Show last 2 exchanges
            print(f"  {i+1}. User: {exchange.get('user', '')[:40]}...")
            print(f"     Aara: {exchange.get('Aara', '')[:40]}...")
        
        # Run the workflow
        response = run_workflow(request.message, chat_history)
        
        # Store conversation if conversation_id is provided
        if request.conversation_id:
            if request.conversation_id not in conversations:
                conversations[request.conversation_id] = []
            conversations[request.conversation_id].append({
                "user": request.message,
                "Aara": response
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
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=args.port,
        reload=True,
        log_level="info"
    ) 