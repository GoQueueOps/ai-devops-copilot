from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes import logs
from db.database import init_db
import os

app = FastAPI(
    title="AI DevOps Copilot",
    description="AI-powered incident analysis for DevOps teams",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(logs.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/")
def serve_frontend():
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')
    return FileResponse(os.path.normpath(frontend_path))