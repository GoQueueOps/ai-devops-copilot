from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_analyzer import analyze_log

router = APIRouter()

class LogRequest(BaseModel):
    log_text: str

class AnalysisResponse(BaseModel):
    cause: str
    fix: str
    severity: str

@router.post("/analyze-log", response_model=AnalysisResponse)
def analyze_log_route(request: LogRequest):
    try:
        result = analyze_log(request.log_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))