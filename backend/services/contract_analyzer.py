"""Contract analysis service using Gemma 4."""

import json
from pathlib import Path
from backend.ollama_client import chat

SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "contract_system.txt").read_text()


LANGUAGE_NAMES = {
    "en": "English", "es": "Spanish", "zh": "Chinese (Simplified)",
    "vi": "Vietnamese", "ko": "Korean", "tl": "Tagalog",
    "ar": "Arabic", "fr": "French", "ru": "Russian", "hi": "Hindi",
}


async def analyze_contract(content: str, document_type: str = "", language: str = "en") -> dict:
    """Analyze a contract or legal document using Gemma 4."""
    user_prompt = f"Analyze the following document and explain it in plain language:\n\n---\n{content}\n---"
    if document_type:
        user_prompt += f"\n\nThe user believes this is a: {document_type}"
    if language != "en" and language in LANGUAGE_NAMES:
        lang_name = LANGUAGE_NAMES[language]
        user_prompt += f"\n\nIMPORTANT: Respond entirely in {lang_name}. All explanations, red flags, actions, and alternatives must be in {lang_name}."

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
        "document_type": "Unknown",
        "summary": text[:500],
        "key_terms": [],
        "flagged_items": [],
        "hidden_costs": [],
        "overall_assessment": text,
        "questions_to_ask": [],
    }
