"""Scam scanner API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.scam_analyzer import analyze_message

router = APIRouter(prefix="/api/scan", tags=["scanner"])


class ScanRequest(BaseModel):
    content: str
    context: str = ""


class ScanResponse(BaseModel):
    trust_score: int
    risk_level: str
    scam_type: str
    red_flags: list[str]
    explanation: str
    recommended_actions: list[str]
    safe_alternatives: str


@router.post("", response_model=ScanResponse)
async def scan_message(req: ScanRequest):
    """Analyze a message, email, or text for scam indicators."""
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    if len(req.content) > 50000:
        raise HTTPException(status_code=400, detail="Content exceeds 50,000 character limit")

    result = await analyze_message(req.content, req.context)
    return ScanResponse(
        trust_score=result.get("trust_score", 50),
        risk_level=result.get("risk_level", "UNCERTAIN"),
        scam_type=result.get("scam_type", "Unknown"),
        red_flags=result.get("red_flags", []),
        explanation=result.get("explanation", ""),
        recommended_actions=result.get("recommended_actions", []),
        safe_alternatives=result.get("safe_alternatives", ""),
    )
