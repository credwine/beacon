"""Scam analysis service using Gemma 4 with structured output via function calling."""

import json
from pathlib import Path
from backend.ollama_client import chat

SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "scam_system.txt").read_text()

SCAM_ANALYSIS_TOOL = {
    "type": "function",
    "function": {
        "name": "report_scam_analysis",
        "description": "Report the results of analyzing a message for scam indicators",
        "parameters": {
            "type": "object",
            "properties": {
                "trust_score": {
                    "type": "integer",
                    "description": "Trust score from 0 (dangerous) to 100 (safe)",
                    "minimum": 0,
                    "maximum": 100,
                },
                "risk_level": {
                    "type": "string",
                    "enum": ["DANGEROUS", "HIGH_RISK", "SUSPICIOUS", "UNCERTAIN", "LIKELY_SAFE"],
                },
                "scam_type": {
                    "type": "string",
                    "description": "Classification of the scam type",
                },
                "red_flags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of identified red flags",
                },
                "explanation": {
                    "type": "string",
                    "description": "Plain-language explanation for a non-technical person",
                },
                "recommended_actions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Recommended actions to take",
                },
                "safe_alternatives": {
                    "type": "string",
                    "description": "What to do instead if they think it might be legitimate",
                },
            },
            "required": [
                "trust_score", "risk_level", "scam_type", "red_flags",
                "explanation", "recommended_actions", "safe_alternatives",
            ],
        },
    },
}


async def analyze_message(content: str, context: str = "") -> dict:
    """Analyze a message for scam indicators using Gemma 4."""
    user_prompt = f"Analyze the following message for scam or fraud indicators:\n\n---\n{content}\n---"
    if context:
        user_prompt += f"\n\nAdditional context from the user: {context}"

    messages = [{"role": "user", "content": user_prompt}]

    # Try function calling first
    try:
        result = await chat(
            messages=messages,
            system=SYSTEM_PROMPT,
            tools=[SCAM_ANALYSIS_TOOL],
        )
        msg = result.get("message", {})

        # Check if model used tool calling
        tool_calls = msg.get("tool_calls", [])
        if tool_calls:
            args = tool_calls[0].get("function", {}).get("arguments", {})
            if args and "trust_score" in args:
                return args

        # Fall back to parsing JSON from content
        content_text = msg.get("content", "")
        if content_text:
            return _extract_json(content_text)
    except Exception:
        pass

    # Fallback: direct generation without tools
    result = await chat(messages=messages, system=SYSTEM_PROMPT)
    content_text = result.get("message", {}).get("content", "")
    return _extract_json(content_text)


def _extract_json(text: str) -> dict:
    """Extract JSON from model response text."""
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find JSON block in markdown
    for marker in ["```json", "```"]:
        if marker in text:
            start = text.index(marker) + len(marker)
            end = text.index("```", start)
            try:
                return json.loads(text[start:end].strip())
            except (json.JSONDecodeError, ValueError):
                pass

    # Try to find JSON object in text
    brace_start = text.find("{")
    brace_end = text.rfind("}")
    if brace_start != -1 and brace_end != -1:
        try:
            return json.loads(text[brace_start:brace_end + 1])
        except json.JSONDecodeError:
            pass

    # Return raw text as explanation if all parsing fails
    return {
        "trust_score": 50,
        "risk_level": "UNCERTAIN",
        "scam_type": "Unknown",
        "red_flags": [],
        "explanation": text,
        "recommended_actions": ["Review the full analysis above"],
        "safe_alternatives": "Contact the supposed sender through their official website or phone number",
    }
