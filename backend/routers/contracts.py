"""Contract analysis API endpoints."""

import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.services.contract_analyzer import analyze_contract

router = APIRouter(prefix="/api/contract", tags=["contracts"])


class ContractRequest(BaseModel):
    content: str = ""
    document_type: str = ""
    language: str = "en"
    image: str = ""  # Base64-encoded image for camera/photo analysis


@router.post("")
async def analyze(req: ContractRequest):
    """Analyze a contract or legal document in plain language.

    Supports text, file upload, or camera photo (base64 image).
    """
    if not req.content.strip() and not req.image:
        raise HTTPException(status_code=400, detail="Provide document text or an image")
    if len(req.content) > 100000:
        raise HTTPException(status_code=400, detail="Content exceeds 100,000 character limit")

    try:
        result = await analyze_contract(req.content, req.document_type, req.language, req.image)
        return JSONResponse(content=result)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
