"""Trusted Contact alert API endpoints.

Manages trusted contacts and alert history for Beacon's caregiver
notification system. All data stored locally in JSON files.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.alert_service import (
    get_contacts,
    save_contact,
    delete_contact,
    trigger_alert,
    get_alert_history,
)

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


# ---- Request/Response Models ----

class ContactRequest(BaseModel):
    name: str
    email: str = ""
    phone: str = ""
    relationship: str = "other"


class ContactResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    relationship: str
    created_at: str


class TriggerRequest(BaseModel):
    trust_score: int
    risk_level: str = "DANGEROUS"
    scam_type: str = "Unknown"
    explanation: str = ""
    red_flags: list[str] = []
    recommended_actions: list[str] = []
    safe_alternatives: str = ""


# ---- Endpoints ----

@router.get("/contacts")
async def list_contacts():
    """Return all saved trusted contacts."""
    return get_contacts()


@router.post("/contacts", response_model=ContactResponse, status_code=201)
async def add_contact(req: ContactRequest):
    """Add a new trusted contact."""
    if not req.name.strip():
        raise HTTPException(status_code=400, detail="Contact name is required")
    if not req.email.strip() and not req.phone.strip():
        raise HTTPException(status_code=400, detail="Provide at least an email or phone number")

    contact = save_contact(
        name=req.name,
        email=req.email,
        phone=req.phone,
        relationship=req.relationship,
    )
    return ContactResponse(**contact)


@router.delete("/contacts/{contact_id}")
async def remove_contact(contact_id: str):
    """Remove a trusted contact by ID."""
    removed = delete_contact(contact_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"status": "deleted", "contact": removed}


@router.post("/trigger")
async def trigger_alert_endpoint(req: TriggerRequest):
    """Trigger an alert for a dangerous scan result.

    Called automatically by the frontend when trust_score <= 20.
    Creates a local alert record and logs it. Future: sends SMS/email.
    """
    scan_result = req.model_dump()
    alert = trigger_alert(scan_result)
    if alert is None:
        return {"status": "skipped", "reason": "Not dangerous enough or no contacts configured"}
    return {"status": "triggered", "alert": alert}


@router.get("/history")
async def list_alert_history():
    """Return alert history, newest first."""
    return get_alert_history()
