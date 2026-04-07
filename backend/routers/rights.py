"""Rights navigator API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.rights_navigator import navigate_rights

router = APIRouter(prefix="/api/rights", tags=["rights"])


class RightsRequest(BaseModel):
    situation: str
    category: str = ""


@router.post("")
async def get_rights(req: RightsRequest):
    """Get rights guidance for a specific situation."""
    if not req.situation.strip():
        raise HTTPException(status_code=400, detail="Situation description cannot be empty")
    if len(req.situation) > 10000:
        raise HTTPException(status_code=400, detail="Description exceeds 10,000 character limit")

    return await navigate_rights(req.situation, req.category)
