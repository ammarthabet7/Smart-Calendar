import uvicorn
from backend.main import app

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Starting Smart Calendar Assistant Server")
    print("="*60)
    print("API: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Frontend: http://localhost:8000/static/index.html")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
