from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from backend.agent.agent import appointment_agent
from backend.services.stt_service import stt_service
from backend.services.tts_service import tts_service
import os

# Initialize FastAPI app
app = FastAPI(title="Smart Calendar Assistant", version="1.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend files
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    success: bool
    response: str
    intent: str = None

# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Smart Calendar Assistant",
        "version": "1.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Text chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process text-based chat message"""
    print(f"\n[API] Received message: '{request.message}'")
    
    try:
        result = appointment_agent.process_message(request.message)
        
        return ChatResponse(
            success=result.get('success', False),
            response=result.get('response', 'Error processing request'),
            intent=result.get('intent')
        )
    except Exception as e:
        print(f"[API] Error: {e}")
        return ChatResponse(
            success=False,
            response="Sorry, I encountered an error processing your request."
        )

# Voice conversation endpoint
@app.post("/voice")
async def voice_conversation():
    """Handle voice-based conversation (STT -> Agent -> TTS)"""
    print("\n[API] Starting voice conversation...")
    
    try:
        # Step 1: Listen to user
        print("[API] Listening for user input...")
        user_text = stt_service.listen_once()
        
        if not user_text:
            return {
                "success": False,
                "error": "No speech detected"
            }
        
        print(f"[API] User said: '{user_text}'")
        
        # Step 2: Process with agent
        result = appointment_agent.process_message(user_text)
        
        return {
            "success": result.get('success', False),
            "user_message": user_text,
            "agent_response": result.get('response'),
            "intent": result.get('intent')
        }
        
    except Exception as e:
        print(f"[API] Error in voice conversation: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time communication"""
    await websocket.accept()
    print("[WS] Client connected")
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"[WS] Received: '{data}'")
            
            result = appointment_agent.process_message(data)
            
            await websocket.send_json({
                "type": "response",
                "message": result.get('response'),
                "intent": result.get('intent'),
                "success": result.get('success')
            })
            
    except WebSocketDisconnect:
        print("[WS] Client disconnected")
    except Exception as e:
        print(f"[WS] Error: {e}")

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("Starting Smart Calendar Assistant Server")
    print("="*60)
    print("API: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("Frontend: http://localhost:8000/static/index.html")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
