"""Server-Sent Events (SSE) streaming endpoints for real-time AI analysis.

These endpoints mirror the non-streaming counterparts but stream tokens
as they arrive from Gemma 4 via Ollama, so users see analysis appearing
in real-time rather than waiting 30+ seconds for a complete response.

SSE event types:
  - prescreen: instant rule-based red flags (scan endpoint only)
  - token: individual token from the LLM as it generates
  - done: signals the stream is complete
"""

import json
import traceback
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from backend.ollama_client import chat_stream
from backend.services.prescreener import prescreen

# Load system prompts once at module level
_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
SCAM_SYSTEM_PROMPT = (_PROMPTS_DIR / "scam_system.txt").read_text()
CONTRACT_SYSTEM_PROMPT = (_PROMPTS_DIR / "contract_system.txt").read_text()
RIGHTS_SYSTEM_PROMPT = (_PROMPTS_DIR / "rights_system.txt").read_text()

router = APIRouter(prefix="/api/stream", tags=["streaming"])


# ---------------------------------------------------------------------------
# Request models (mirror the non-streaming counterparts)
# ---------------------------------------------------------------------------

class StreamScanRequest(BaseModel):
    content: str = ""
    context: str = ""
    image: str = ""  # Base64-encoded image for multimodal analysis


class StreamContractRequest(BaseModel):
    content: str
    document_type: str = ""


class StreamRightsRequest(BaseModel):
    situation: str
    category: str = ""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sse_event(event: str, data: dict) -> str:
    """Format a single SSE event."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


# ---------------------------------------------------------------------------
# Streaming endpoints
# ---------------------------------------------------------------------------

@router.post("/scan")
async def stream_scan(req: StreamScanRequest):
    """Stream scam analysis tokens in real-time via SSE.

    Pipeline:
      1. Immediately emits a 'prescreen' event with rule-based red flags.
      2. Streams 'token' events as Gemma 4 generates the analysis.
      3. Emits a 'done' event when the LLM finishes.
    """
    if not req.content.strip() and not req.image:
        raise HTTPException(status_code=400, detail="Provide text content or an image to analyze")
    if len(req.content) > 50000:
        raise HTTPException(status_code=400, detail="Content exceeds 50,000 character limit")

    # Build the user prompt (same logic as scam_analyzer.py)
    if req.image:
        user_prompt = (
            "Analyze this image for scam or fraud indicators. "
            "Extract any text visible in the image and evaluate it "
            "for signs of fraud, phishing, or manipulation."
        )
        if req.content:
            user_prompt += f"\n\nThe user also provided this text context:\n---\n{req.content}\n---"
        if req.context:
            user_prompt += f"\n\nAdditional context: {req.context}"
        messages = [{"role": "user", "content": user_prompt, "images": [req.image]}]
    else:
        user_prompt = f"Analyze the following message for scam or fraud indicators:\n\n---\n{req.content}\n---"
        if req.context:
            user_prompt += f"\n\nAdditional context from the user: {req.context}"
        messages = [{"role": "user", "content": user_prompt}]

    # Run prescreen synchronously (it is pure regex, sub-millisecond)
    prescreen_result = prescreen(req.content) if req.content.strip() else {
        "instant_flags": [],
        "preliminary_score": 100,
        "flag_count": 0,
    }

    async def event_generator():
        # Stage 1: instant prescreen
        yield _sse_event("prescreen", prescreen_result)

        # Stage 2: stream LLM tokens
        try:
            async for token in chat_stream(messages=messages, system=SCAM_SYSTEM_PROMPT):
                yield _sse_event("token", {"text": token})
        except Exception:
            traceback.print_exc()
            yield _sse_event("token", {"text": "[Error: AI analysis failed. Please try again.]"})

        # Stage 3: done
        yield _sse_event("done", {"status": "complete"})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/contract")
async def stream_contract(req: StreamContractRequest):
    """Stream contract analysis tokens in real-time via SSE."""
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    if len(req.content) > 100000:
        raise HTTPException(status_code=400, detail="Content exceeds 100,000 character limit")

    user_prompt = f"Analyze the following document and explain it in plain language:\n\n---\n{req.content}\n---"
    if req.document_type:
        user_prompt += f"\n\nThe user believes this is a: {req.document_type}"

    messages = [{"role": "user", "content": user_prompt}]

    async def event_generator():
        try:
            async for token in chat_stream(messages=messages, system=CONTRACT_SYSTEM_PROMPT):
                yield _sse_event("token", {"text": token})
        except Exception:
            traceback.print_exc()
            yield _sse_event("token", {"text": "[Error: AI analysis failed. Please try again.]"})

        yield _sse_event("done", {"status": "complete"})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/rights")
async def stream_rights(req: StreamRightsRequest):
    """Stream rights analysis tokens in real-time via SSE."""
    if not req.situation.strip():
        raise HTTPException(status_code=400, detail="Situation description cannot be empty")
    if len(req.situation) > 10000:
        raise HTTPException(status_code=400, detail="Description exceeds 10,000 character limit")

    user_prompt = f"I need help understanding my rights in this situation:\n\n{req.situation}"
    if req.category:
        user_prompt += f"\n\nThis relates to: {req.category}"

    messages = [{"role": "user", "content": user_prompt}]

    async def event_generator():
        try:
            async for token in chat_stream(messages=messages, system=RIGHTS_SYSTEM_PROMPT):
                yield _sse_event("token", {"text": token})
        except Exception:
            traceback.print_exc()
            yield _sse_event("token", {"text": "[Error: AI analysis failed. Please try again.]"})

        yield _sse_event("done", {"status": "complete"})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
