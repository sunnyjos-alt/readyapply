import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="ReadyApply API")

# Define base directory absolute path
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Mount static files if frontend folder exists
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
async def read_root():
    # Look for index.html in the frontend directory
    index_file = FRONTEND_DIR / "index.html"
    
    # Fallback check for root directory if not in frontend/
    if not index_file.exists():
        index_file = BASE_DIR / "index.html"
        
    if index_file.exists():
        return FileResponse(index_file)
    
    return {"message": f"index.html not found. Checked: {FRONTEND_DIR / 'index.html'} and {BASE_DIR / 'index.html'}"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "ReadyApply"}
