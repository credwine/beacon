"""Beacon Guard -- Zero-UI Silent Security Agent.

Runs in the background, captures screenshots periodically, and uses Gemma 4
vision to detect phishing, dark patterns, scam pop-ups, and social engineering
in real-time. Sends a system notification only when a threat is detected.

The user never interacts with this. It just watches and protects.

Usage:
    python -m guard.beacon_guard              # Start monitoring
    python -m guard.beacon_guard --interval 5 # Check every 5 seconds
    python -m guard.beacon_guard --threshold 80 # Alert at 80% confidence
"""

import argparse
import base64
import hashlib
import io
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

import httpx

try:
    from PIL import ImageGrab, Image
except ImportError:
    print("Install Pillow: pip install Pillow")
    sys.exit(1)

try:
    from plyer import notification as plyer_notification
except ImportError:
    plyer_notification = None

try:
    from win10toast import ToastNotifier
    _toaster = ToastNotifier()
except ImportError:
    _toaster = None

# ---- Configuration ----

OLLAMA_URL = "http://localhost:11434"
GEMMA_MODEL = "gemma4:e2b"  # E2B for vision -- smaller footprint for background monitoring
ALERT_THRESHOLD = 85  # Only notify if threat confidence >= this
CHECK_INTERVAL = 7    # Seconds between checks
CHANGE_THRESHOLD = 5  # Percentage of pixels that must change to trigger analysis
LOG_DIR = Path(__file__).parent / "logs"
ALERT_LOG = Path(__file__).parent / "alert_history.json"

GUARD_SYSTEM_PROMPT = """You are Beacon Guard, an elite local security agent monitoring the user's screen for threats.

Your job: Analyze this screenshot for ANY of the following threats:

1. PHISHING: Fake login pages, URL mismatches (site claims to be a bank but URL is wrong), credential harvesting forms
2. DARK PATTERNS: Fake urgency timers, hidden unsubscribe buttons, misleading "X" close buttons that actually confirm
3. SCAM POP-UPS: "Your computer is infected" alerts, fake virus warnings, tech support scams
4. SOCIAL ENGINEERING: Emails/messages using urgency, authority impersonation, emotional manipulation
5. SUSPICIOUS URLS: .xyz, .tk domains, IP-address URLs, URL shorteners on sensitive forms
6. PII HARVESTING: Forms asking for SSN, full credit card, PIN in suspicious contexts

RESPONSE FORMAT -- You MUST respond in valid JSON:
{
  "threat_detected": true/false,
  "confidence": 0-100,
  "threat_type": "phishing|dark_pattern|scam_popup|social_engineering|suspicious_url|pii_harvesting|none",
  "severity": "critical|high|medium|low|none",
  "description": "One-sentence description of what you found",
  "details": "Specific elements that triggered the alert (URL, button text, etc.)",
  "recommendation": "What the user should do right now"
}

RULES:
- Only flag REAL threats. Normal websites, apps, and emails are NOT threats.
- A login page on the REAL domain (google.com, bankofamerica.com) is SAFE.
- Be conservative. False positives destroy trust. Only alert when you are confident.
- Focus on the URL bar, form fields, pop-up text, and call-to-action buttons.
- If the screen shows a normal desktop, app, or game, respond with threat_detected: false."""


# ---- Logging ----

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [Guard] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("beacon-guard")


# ---- Screenshot & Change Detection ----

def capture_screen() -> Image.Image:
    """Capture the current screen."""
    return ImageGrab.grab()


def image_to_base64(img: Image.Image, max_size: int = 1280) -> str:
    """Resize and convert image to base64 for Gemma 4 vision."""
    # Resize to keep token usage reasonable
    ratio = min(max_size / img.width, max_size / img.height, 1.0)
    if ratio < 1.0:
        img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=75)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def image_hash(img: Image.Image) -> str:
    """Quick perceptual hash for change detection."""
    small = img.resize((16, 16), Image.LANCZOS).convert("L")
    pixels = list(small.getdata())
    avg = sum(pixels) / len(pixels)
    return "".join("1" if p > avg else "0" for p in pixels)


def screen_changed(hash1: str, hash2: str, threshold: float = 5.0) -> bool:
    """Check if screen changed significantly (hamming distance as percentage)."""
    if not hash1 or not hash2:
        return True
    diff = sum(a != b for a, b in zip(hash1, hash2))
    pct = (diff / len(hash1)) * 100
    return pct >= threshold


# ---- Gemma 4 Analysis ----

def analyze_screenshot(img_b64: str) -> dict:
    """Send screenshot to Gemma 4 for threat analysis."""
    try:
        response = httpx.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": GEMMA_MODEL,
                "messages": [
                    {"role": "system", "content": GUARD_SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": "Analyze this screenshot for security threats.",
                        "images": [img_b64],
                    },
                ],
                "stream": False,
                "options": {
                    "num_predict": 1024,
                    "temperature": 0.2,
                },
            },
            timeout=120.0,
        )
        response.raise_for_status()
        content = response.json().get("message", {}).get("content", "")
        return extract_json(content)
    except Exception as e:
        log.error(f"Analysis failed: {e}")
        return {"threat_detected": False, "confidence": 0, "error": str(e)}


def extract_json(text: str) -> dict:
    """Extract JSON from model response."""
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

    return {"threat_detected": False, "confidence": 0, "raw": text}


# ---- Notification ----

def send_alert(result: dict):
    """Send system notification for detected threat.

    Tries multiple notification methods for cross-platform reliability:
    1. win10toast (Windows 10/11 native toast)
    2. plyer (cross-platform)
    3. PowerShell fallback (Windows)
    """
    severity = result.get("severity", "high").upper()
    threat_type = result.get("threat_type", "unknown").replace("_", " ").title()
    description = result.get("description", "Suspicious activity detected")
    recommendation = result.get("recommendation", "Close the suspicious page")

    title = f"Beacon Guard -- {severity} THREAT"
    message = f"{threat_type}: {description}. {recommendation}"

    log.warning(f"ALERT: {title} -- {message}")

    # Method 0: Persistent always-on-top window (stays until dismissed)
    try:
        from guard.alert_window import show_alert
        show_alert(title=f"{threat_type} detected", message=f"{description}. {recommendation}", severity=result.get("severity", "high"))
    except Exception:
        pass

    # Method 1: win10toast backup
    if _toaster:
        try:
            icon_path = str(Path(__file__).parent.parent / "frontend" / "assets" / "beacon.ico")
            _toaster.show_toast(
                title,
                message,
                icon_path=icon_path if Path(icon_path).exists() else None,
                duration=30,
                threaded=True,
            )
            return
        except Exception as e:
            log.debug(f"win10toast failed: {e}")

    # Method 2: plyer (cross-platform)
    if plyer_notification:
        try:
            plyer_notification.notify(
                title=title,
                message=message,
                app_name="Beacon Guard",
                timeout=10,
            )
            return
        except Exception as e:
            log.debug(f"plyer failed: {e}")

    # Method 3: PowerShell fallback (Windows)
    try:
        import subprocess
        # Escape quotes for PowerShell
        safe_title = title.replace("'", "''")
        safe_msg = message.replace("'", "''")
        ps_cmd = f"""
        Add-Type -AssemblyName System.Windows.Forms;
        $n = New-Object System.Windows.Forms.NotifyIcon;
        $n.Icon = [System.Drawing.SystemIcons]::Warning;
        $n.BalloonTipTitle = '{safe_title}';
        $n.BalloonTipText = '{safe_msg}';
        $n.BalloonTipIcon = 'Error';
        $n.Visible = $true;
        $n.ShowBalloonTip(10000);
        Start-Sleep -Seconds 11;
        $n.Dispose();
        """
        subprocess.Popen(
            ["powershell", "-Command", ps_cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass  # Log is the last resort


def save_alert(result: dict):
    """Append alert to local history file."""
    history = []
    if ALERT_LOG.exists():
        try:
            history = json.loads(ALERT_LOG.read_text())
        except (json.JSONDecodeError, OSError):
            pass

    history.append({
        "timestamp": datetime.now().isoformat(),
        **result,
    })

    # Keep last 100 alerts
    history = history[-100:]
    ALERT_LOG.write_text(json.dumps(history, indent=2))


# ---- Main Loop ----

def run_guard(interval: int = CHECK_INTERVAL, threshold: int = ALERT_THRESHOLD,
              change_pct: float = CHANGE_THRESHOLD):
    """Main guard loop -- silent, continuous screen monitoring."""

    log.info("=" * 50)
    log.info("Beacon Guard -- Zero-UI Silent Security Agent")
    log.info(f"Check interval: {interval}s")
    log.info(f"Alert threshold: {threshold}% confidence")
    log.info(f"Change detection: {change_pct}% pixel change")
    log.info(f"Model: {GEMMA_MODEL}")
    log.info("=" * 50)
    log.info("Monitoring started. You won't see anything unless a threat is found.")
    log.info("")

    LOG_DIR.mkdir(exist_ok=True)
    last_hash = ""
    checks = 0
    alerts = 0

    while True:
        try:
            # Capture screen
            screenshot = capture_screen()
            current_hash = image_hash(screenshot)

            # Change detection -- skip if screen hasn't changed
            if not screen_changed(last_hash, current_hash, change_pct):
                time.sleep(interval)
                continue

            last_hash = current_hash
            checks += 1

            # Convert to base64 for Gemma 4
            img_b64 = image_to_base64(screenshot)

            # Analyze with Gemma 4 vision
            log.info(f"Screen changed -- analyzing (check #{checks})...")
            result = analyze_screenshot(img_b64)

            threat = result.get("threat_detected", False)
            confidence = result.get("confidence", 0)

            if threat and confidence >= threshold:
                alerts += 1
                log.warning(f"THREAT DETECTED (confidence: {confidence}%)")
                send_alert(result)
                save_alert(result)
            elif threat:
                log.info(f"Low-confidence threat ({confidence}%) -- suppressed")
            else:
                log.info(f"Clean (check #{checks}, {alerts} alerts total)")

        except KeyboardInterrupt:
            log.info(f"\nGuard stopped. {checks} checks, {alerts} alerts.")
            break
        except Exception as e:
            log.error(f"Error: {e}")

        time.sleep(interval)


# ---- Entry Point ----

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Beacon Guard -- Silent Security Agent")
    parser.add_argument("--interval", type=int, default=CHECK_INTERVAL,
                        help=f"Seconds between checks (default: {CHECK_INTERVAL})")
    parser.add_argument("--threshold", type=int, default=ALERT_THRESHOLD,
                        help=f"Alert confidence threshold (default: {ALERT_THRESHOLD})")
    parser.add_argument("--change", type=float, default=CHANGE_THRESHOLD,
                        help=f"Screen change threshold %% (default: {CHANGE_THRESHOLD})")
    parser.add_argument("--model", type=str, default=GEMMA_MODEL,
                        help=f"Ollama model (default: {GEMMA_MODEL})")
    args = parser.parse_args()

    GEMMA_MODEL = args.model
    run_guard(interval=args.interval, threshold=args.threshold, change_pct=args.change)
