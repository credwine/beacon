"""Trusted Contact alert service -- local-only alert system.

Manages trusted contacts and alert history, stored in local JSON files.
When a dangerous scam is detected (trust_score <= 20), an alert record is
created and saved locally. Future versions can extend this to send SMS/email.
"""

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger("beacon.alerts")

DATA_DIR = Path(__file__).parent.parent.parent / "data"
CONTACTS_FILE = DATA_DIR / "trusted_contacts.json"
HISTORY_FILE = DATA_DIR / "alert_history.json"


def _ensure_data_dir():
    """Create the data directory if it does not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path) -> list:
    """Read a JSON array from a file, returning empty list if missing."""
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _write_json(path: Path, data: list):
    """Write a JSON array to a file."""
    _ensure_data_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ---- Contact Management ----

def get_contacts() -> list[dict]:
    """Return all saved trusted contacts."""
    return _read_json(CONTACTS_FILE)


def save_contact(
    name: str,
    email: str = "",
    phone: str = "",
    relationship: str = "other",
) -> dict:
    """Save a new trusted contact. Returns the created contact dict."""
    contacts = _read_json(CONTACTS_FILE)
    contact = {
        "id": str(uuid.uuid4()),
        "name": name.strip(),
        "email": email.strip(),
        "phone": phone.strip(),
        "relationship": relationship,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    contacts.append(contact)
    _write_json(CONTACTS_FILE, contacts)
    logger.info("Saved trusted contact: %s (%s)", contact["name"], contact["id"])
    return contact


def delete_contact(contact_id: str) -> Optional[dict]:
    """Remove a contact by ID. Returns the removed contact or None."""
    contacts = _read_json(CONTACTS_FILE)
    removed = None
    updated = []
    for c in contacts:
        if c.get("id") == contact_id:
            removed = c
        else:
            updated.append(c)
    if removed:
        _write_json(CONTACTS_FILE, updated)
        logger.info("Deleted trusted contact: %s (%s)", removed["name"], removed["id"])
    return removed


# ---- Alert Triggering ----

def trigger_alert(scan_result: dict, contacts: list[dict] | None = None) -> dict | None:
    """Create an alert record when a dangerous scan is detected.

    Only triggers for trust_score <= 20 (DANGEROUS). Saves the alert to
    local history. Returns the alert record, or None if not dangerous enough.

    Future: this is where SMS/email sending would be wired in.
    """
    trust_score = scan_result.get("trust_score", 100)
    if trust_score > 20:
        return None

    if contacts is None:
        contacts = get_contacts()

    if not contacts:
        logger.info("Dangerous scam detected (score=%d) but no trusted contacts configured", trust_score)
        return None

    contact_names = [c.get("name", "Unknown") for c in contacts]

    alert = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trust_score": trust_score,
        "risk_level": scan_result.get("risk_level", "DANGEROUS"),
        "scam_type": scan_result.get("scam_type", "Unknown"),
        "explanation": scan_result.get("explanation", ""),
        "red_flags": scan_result.get("red_flags", []),
        "contacts_notified": contact_names,
        "delivery_method": "local_log",  # future: "sms", "email"
        "status": "logged",  # future: "sent", "delivered", "failed"
    }

    # Save to history
    history = _read_json(HISTORY_FILE)
    history.insert(0, alert)  # newest first
    # Keep at most 200 alert records
    if len(history) > 200:
        history = history[:200]
    _write_json(HISTORY_FILE, history)

    logger.warning(
        "ALERT triggered -- trust_score=%d, scam_type=%s, contacts=%s",
        trust_score,
        alert["scam_type"],
        ", ".join(contact_names),
    )

    return alert


# ---- Alert History ----

def get_alert_history() -> list[dict]:
    """Return alert history, newest first."""
    return _read_json(HISTORY_FILE)
