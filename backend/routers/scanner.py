"""Scam scanner API endpoints -- text and image (multimodal) analysis.

Two-stage pipeline:
  1. /api/scan/prescreen -- instant rule-based red flags (<1ms)
  2. /api/scan -- full Gemma 4 LLM analysis (10-30s)
"""

import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.services.scam_analyzer import analyze_message
from backend.services.prescreener import prescreen

router = APIRouter(prefix="/api/scan", tags=["scanner"])


class ScanRequest(BaseModel):
    content: str = ""
    context: str = ""
    image: str = ""  # Base64-encoded image for multimodal analysis
    language: str = "en"


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
    """Analyze a message, email, text, or screenshot for scam indicators.

    Supports text-only or multimodal (text + image) analysis.
    Send base64-encoded image in the 'image' field for screenshot scanning.
    """
    if not req.content.strip() and not req.image:
        raise HTTPException(status_code=400, detail="Provide text content or an image to analyze")
    if len(req.content) > 50000:
        raise HTTPException(status_code=400, detail="Content exceeds 50,000 character limit")

    try:
        result = await analyze_message(req.content, req.context, req.image, req.language)
        return ScanResponse(
            trust_score=result.get("trust_score", 50),
            risk_level=result.get("risk_level", "UNCERTAIN"),
            scam_type=result.get("scam_type", "Unknown"),
            red_flags=result.get("red_flags", []),
            explanation=result.get("explanation", ""),
            recommended_actions=result.get("recommended_actions", []),
            safe_alternatives=result.get("safe_alternatives", ""),
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


class PrescreenRequest(BaseModel):
    content: str


@router.post("/prescreen")
async def prescreen_message(req: PrescreenRequest):
    """Instant rule-based pre-screening (<1ms).

    Stage 1 of Beacon's two-stage pipeline. Returns immediate red flags
    while the full Gemma 4 analysis runs in the background.
    """
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    return prescreen(req.content)
