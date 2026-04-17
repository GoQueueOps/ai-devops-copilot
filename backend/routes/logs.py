from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_analyzer import analyze_log
from services.alert_service import send_alert
from db.database import save_incident, get_recent_incidents

router = APIRouter()

ALERT_SEVERITIES = ["high", "critical"]

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
        
        print(f"Severity: {result['severity']}")
        print(f"Will alert: {result['severity'] in ALERT_SEVERITIES}")

        save_incident(
            log_text=request.log_text,
            cause=result["cause"],
            fix=result["fix"],
            severity=result["severity"]
        )

        if result["severity"] in ALERT_SEVERITIES:
            send_alert(
                log_text=request.log_text,
                cause=result["cause"],
                fix=result["fix"],
                severity=result["severity"]
            )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/incidents")
def get_incidents():
    try:
        incidents = get_recent_incidents()
        return [
            {
                "id": i.id,
                "log_text": i.log_text,
                "cause": i.cause,
                "fix": i.fix,
                "severity": i.severity,
                "created_at": i.created_at.isoformat()
            }
            for i in incidents
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))