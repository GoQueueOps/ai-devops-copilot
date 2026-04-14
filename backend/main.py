from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import logs

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

app.include_router(logs.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}