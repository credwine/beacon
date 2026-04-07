"""Contract analysis API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.contract_analyzer import analyze_contract

router = APIRouter(prefix="/api/contract", tags=["contracts"])


class ContractRequest(BaseModel):
    content: str
    document_type: str = ""


@router.post("")
async def analyze(req: ContractRequest):
    """Analyze a contract or legal document in plain language."""
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    if len(req.content) > 100000:
        raise HTTPException(status_code=400, detail="Content exceeds 100,000 character limit")

    return await analyze_contract(req.content, req.document_type)
