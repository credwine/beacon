"""Lightweight rule-based pre-screener for instant scam detection.

This runs in milliseconds before the full Gemma 4 analysis, providing
immediate feedback on obvious scam indicators. It forms the first stage
of Beacon's multi-model pipeline:

  1. Pre-screener (rules, <1ms) -> instant red flags
  2. Gemma 4 (LLM, ~10-30s) -> deep analysis with explanations

This two-stage approach gives users instant gratification while the AI
works on the comprehensive analysis.
"""

import re

# Known scam patterns (case-insensitive)
URGENCY_PATTERNS = [
    r"\b(act now|immediately|urgent|right away|don'?t delay)\b",
    r"\b(limited time|expires? (today|soon|in \d+))\b",
    r"\b(final (notice|warning|chance))\b",
    r"\b(within \d+ hours?|last chance)\b",
]

AUTHORITY_PATTERNS = [
    r"\b(irs|social security|ssa|fbi|police|sheriff|department of)\b",
    r"\b(apple (id|security)|microsoft (security|support))\b",
    r"\b(bank.{0,15}security|account.{0,15}(suspended|locked|compromised))\b",
    r"\b(warrant.{0,15}(arrest|issued))\b",
]

PAYMENT_PATTERNS = [
    r"\b(gift card|itunes card|google play card|steam card)\b",
    r"\b(western union|moneygram|wire transfer|bitcoin|crypto)\b",
    r"\b(processing fee|advance fee|shipping fee)\b",
    r"\b(send \$?\d+|pay \$?\d+|transfer \$?\d+)\b",
]

GREED_PATTERNS = [
    r"\b(you('ve)? (won|been selected|inherited))\b",
    r"\b(lottery|sweepstakes|jackpot|prize)\b",
    r"\b(million (dollars|usd|\$))\b",
    r"\b(congratulations!?|winner!?)\b",
]

SUSPICIOUS_URL_PATTERNS = [
    r"https?://[^\s]*\.(xyz|tk|ml|ga|cf|gq|top|club|work)\b",
    r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
    r"https?://[^\s]*-verify[^\s]*",
    r"https?://[^\s]*secure-login[^\s]*",
    r"https?://[^\s]*account-confirm[^\s]*",
]

ISOLATION_PATTERNS = [
    r"\b(don'?t tell (anyone|your|no one))\b",
    r"\b(keep this (confidential|secret|between))\b",
    r"\b(this is private|do not share)\b",
]


def prescreen(text: str) -> dict:
    """Run fast rule-based pre-screening on a message.

    Returns instant red flags and a preliminary risk score.
    This is NOT a replacement for Gemma 4 analysis -- it's a fast first pass.
    """
    text_lower = text.lower()
    flags = []
    score_deductions = 0

    # Check each pattern category
    for pattern in URGENCY_PATTERNS:
        if re.search(pattern, text_lower):
            flags.append("Urgency/pressure language detected")
            score_deductions += 15
            break

    for pattern in AUTHORITY_PATTERNS:
        if re.search(pattern, text_lower):
            flags.append("Possible authority impersonation")
            score_deductions += 20
            break

    for pattern in PAYMENT_PATTERNS:
        if re.search(pattern, text_lower):
            flags.append("Unusual payment method requested")
            score_deductions += 20
            break

    for pattern in GREED_PATTERNS:
        if re.search(pattern, text_lower):
            flags.append("Too-good-to-be-true offer")
            score_deductions += 15
            break

    for pattern in SUSPICIOUS_URL_PATTERNS:
        if re.search(pattern, text_lower):
            flags.append("Suspicious URL detected")
            score_deductions += 25
            break

    for pattern in ISOLATION_PATTERNS:
        if re.search(pattern, text_lower):
            flags.append("Isolation tactics detected")
            score_deductions += 15
            break

    preliminary_score = max(0, 100 - score_deductions)

    return {
        "instant_flags": flags,
        "preliminary_score": preliminary_score,
        "flag_count": len(flags),
    }
