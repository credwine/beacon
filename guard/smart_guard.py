"""Beacon Guard -- Smart Mode.

Hybrid approach that works on ANY device:
1. Monitors active window title + clipboard for suspicious content (instant, zero memory)
2. Runs rule-based pattern matching on detected text (instant)
3. Only calls Gemma 4 LLM when rules flag something AND model is available (optional)

Works on 8GB laptops. No Tesseract. No heavy dependencies.

Usage:
    python -m guard.smart_guard
"""

import argparse
import ctypes
import json
import logging
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None

try:
    from win10toast import ToastNotifier
    _toaster = ToastNotifier()
except ImportError:
    _toaster = None

# ---- Config ----

CHECK_INTERVAL = 3
ALERT_LOG = Path(__file__).parent / "alert_history.json"

# ---- Scam Patterns ----

PATTERNS = {
    "urgency": [
        r"\b(act now|immediately|urgent|right away)\b",
        r"\b(limited time|expires? (today|soon))\b",
        r"\b(final (notice|warning|chance))\b",
        r"\b(within \d+ hours?|last chance)\b",
        r"\b(account.{0,20}(suspended|locked|closed|compromised))\b",
        r"\b(verify.{0,15}(immediately|now|today))\b",
    ],
    "authority": [
        r"\b(irs|social security|ssa|fbi|police)\b",
        r"\b(apple.{0,5}(id|security)|microsoft.{0,5}(security|support))\b",
        r"\b(paypal|netflix|amazon).{0,15}(security|verify|suspended)\b",
        r"\b(bank.{0,15}(security|verify|fraud))\b",
    ],
    "payment": [
        r"\b(gift card|itunes card|google play card)\b",
        r"\b(western union|wire transfer|bitcoin|crypto)\b",
        r"\b(update.{0,10}payment|payment.{0,10}(details|method|expired))\b",
        r"\b(credit card.{0,10}(number|expired|update))\b",
    ],
    "phishing": [
        r"\b(click here|click below|tap here)\b",
        r"\b(verify your (identity|account|email))\b",
        r"\b(confirm your (identity|account|password))\b",
        r"\b(unusual (activity|sign.?in|login))\b",
        r"\b(unauthorized (access|activity|transaction))\b",
        r"\b(dear (user|customer|member|valued))\b",
        r"\b(update your (password|credentials|information))\b",
    ],
    "suspicious_url": [
        r"https?://[^\s]*\.(xyz|tk|ml|ga|cf|gq|top|club|work|buzz)",
        r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
        r"https?://[^\s]*-(verify|secure|login|confirm)[^\s]*",
    ],
    "greed": [
        r"\b(you('ve)? (won|been selected|inherited))\b",
        r"\b(lottery|sweepstakes|jackpot|prize)\b",
        r"\b(congratulations!?\s+you)\b",
    ],
}

SEVERITY_MAP = {
    "urgency": 15,
    "authority": 20,
    "payment": 25,
    "phishing": 20,
    "suspicious_url": 25,
    "greed": 15,
}

# ---- Logging ----

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [SmartGuard] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("smart-guard")


# ---- Windows APIs for window title + clipboard ----

def get_active_window_title() -> str:
    """Get the title of the currently focused window."""
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
        return buf.value
    except Exception:
        return ""


def get_clipboard_text() -> str:
    """Get current clipboard text content."""
    try:
        ctypes.windll.user32.OpenClipboard(0)
        try:
            # CF_UNICODETEXT = 13
            handle = ctypes.windll.user32.GetClipboardData(13)
            if handle:
                text = ctypes.c_wchar_p(handle).value
                return text or ""
        finally:
            ctypes.windll.user32.CloseClipboard()
    except Exception:
        return ""


def get_screen_text_from_title_bar() -> str:
    """Extract text clues from the active window title.

    Browser titles often contain the page title + URL info.
    Email clients show sender + subject.
    """
    title = get_active_window_title()
    return title


# ---- Analysis ----

def analyze_text(text: str) -> dict:
    """Run pattern matching against text."""
    if not text or len(text.strip()) < 5:
        return {"threat_detected": False, "confidence": 0, "flags": [], "description": ""}

    text_lower = text.lower()
    flags = []
    matched = []
    score = 0

    for category, patterns in PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                flags.append(f"{category}: {match.group(0)}")
                matched.append(match.group(0))
                score += SEVERITY_MAP.get(category, 10)
                break  # One match per category

    threat = len(flags) >= 2  # Need 2+ categories to alert
    confidence = min(100, score)

    return {
        "threat_detected": threat,
        "confidence": confidence,
        "flags": flags,
        "matched_text": matched,
        "severity": "critical" if score >= 60 else "high" if score >= 40 else "medium" if score >= 20 else "none",
        "description": f"Found {len(flags)} suspicious patterns" if flags else "Clean",
        "recommendation": "Do not click links or enter personal information." if threat else "",
    }


# ---- Notification ----

def send_alert(result: dict, source: str):
    """Send Windows notification."""
    severity = result.get("severity", "high").upper()
    title = f"Beacon Guard -- {severity} THREAT"
    flags = result.get("flags", [])
    message = f"Detected: {', '.join(f.split(': ')[0] for f in flags[:3])}. {result.get('recommendation', '')}"

    log.warning(f"ALERT [{source}]: {title}")
    for f in flags:
        log.warning(f"  {f}")

    if _toaster:
        try:
            icon_path = str(Path(__file__).parent.parent / "frontend" / "assets" / "beacon.ico")
            _toaster.show_toast(
                title, message,
                icon_path=icon_path if Path(icon_path).exists() else None,
                duration=10,
                threaded=True,
            )
        except Exception:
            pass

    # Save to history
    history = []
    if ALERT_LOG.exists():
        try:
            history = json.loads(ALERT_LOG.read_text())
        except Exception:
            pass
    history.append({
        "timestamp": datetime.now().isoformat(),
        "source": source,
        **result,
    })
    ALERT_LOG.write_text(json.dumps(history[-100:], indent=2))


# ---- Main Loop ----

def run_guard(interval: int = CHECK_INTERVAL):
    log.info("=" * 55)
    log.info("Beacon Guard -- Smart Mode")
    log.info("Zero LLM required. Monitors window titles + clipboard.")
    log.info(f"Check interval: {interval}s")
    log.info("Works on any device, even 4GB RAM.")
    log.info("=" * 55)
    log.info("")

    checks = 0
    alerts = 0
    last_title = ""
    last_clipboard = ""

    while True:
        try:
            checks += 1

            # Check 1: Active window title
            title = get_active_window_title()
            if title and title != last_title:
                last_title = title
                result = analyze_text(title)
                if result["threat_detected"]:
                    alerts += 1
                    send_alert(result, f"window: {title[:60]}")
                else:
                    log.info(f"#{checks} Window: \"{title[:50]}\" -- clean")

            # Check 2: Clipboard content (catches copied scam text)
            clipboard = get_clipboard_text()
            if clipboard and clipboard != last_clipboard and len(clipboard) > 20:
                last_clipboard = clipboard
                result = analyze_text(clipboard)
                if result["threat_detected"]:
                    alerts += 1
                    send_alert(result, f"clipboard ({len(clipboard)} chars)")
                elif len(clipboard) > 50:
                    flags_found = len(result.get("flags", []))
                    log.info(f"#{checks} Clipboard: {len(clipboard)} chars, {flags_found} flags")

        except KeyboardInterrupt:
            log.info(f"\nStopped. {checks} checks, {alerts} alerts.")
            break
        except Exception as e:
            log.error(f"Error: {e}")

        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Beacon Guard -- Smart Mode (Zero AI)")
    parser.add_argument("--interval", type=int, default=CHECK_INTERVAL)
    args = parser.parse_args()
    run_guard(interval=args.interval)
