from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routes import logs, documents
from db.database import init_db
import os

app = FastAPI(
    title="AI DevOps Copilot",
    description="AI-powered incident analysis for DevOps teams",
    version="0.2.0"
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
app.include_router(documents.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.2.0"}

@app.get("/")
def serve_frontend():
    docker_path = "/app/frontend/index.html"
    local_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')
    )
    if os.path.exists(docker_path):
        return FileResponse(docker_path)
    return FileResponse(local_path)