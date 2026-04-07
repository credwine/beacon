"""Rights navigator service using Gemma 4."""

import json
from pathlib import Path
from backend.ollama_client import chat

SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "rights_system.txt").read_text()


async def navigate_rights(situation: str, category: str = "") -> dict:
    """Help a user understand their rights in a given situation."""
    user_prompt = f"I need help understanding my rights in this situation:\n\n{situation}"
    if category:
        user_prompt += f"\n\nThis relates to: {category}"

    messages = [{"role": "user", "content": user_prompt}]
    result = await chat(messages=messages, system=SYSTEM_PROMPT)
    content_text = result.get("message", {}).get("content", "")
    return _extract_json(content_text)


def _extract_json(text: str) -> dict:
    """Extract JSON from model response text."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    for marker in ["```json", "```"]:
        if marker in text:
            start = text.index(marker) + len(marker)
            end = text.index("```", start)
            try:
                return json.loads(text[start:end].strip())
            except (json.JSONDecodeError, ValueError):
                pass

    brace_start = text.find("{")
    brace_end = text.rfind("}")
    if brace_start != -1 and brace_end != -1:
        try:
            return json.loads(text[brace_start:brace_end + 1])
        except json.JSONDecodeError:
            pass

    return {
        "situation_summary": situation[:200],
        "applicable_rights": [],
        "immediate_actions": [],
        "documentation_needed": [],
        "free_resources": [],
        "warnings": [],
        "timeline": text,
    }
