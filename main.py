import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

# Enable open CORS rules
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_assets"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Path to frontend directory
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

db_store = {}

class ProfileData(BaseModel):
    fullName: str = ""
    dob: str = ""
    category: str = ""
    email: str = ""
    phone: str = ""
    qualification: str = ""

@app.get("/api/health")
def read_root():
    return {"status": "Cloud API Active", "version": "v6"}

@app.post("/api/sync-profile")
def sync_profile(profile: ProfileData):
    db_store["profile"] = profile.dict()
    return {"status": "success", "message": "Profile synced to database!", "data": db_store["profile"]}

@app.get("/api/get-profile")
def get_profile():
    return db_store.get("profile", {})

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), file_type: str = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, f"{file_type}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "success", "message": f"{file_type.capitalize()} saved on server!", "filename": file.filename}

# Serve static frontend files directly from the backend server
@app.get("/")
def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "index.html not found in frontend folder"}