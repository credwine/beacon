"""Beacon Guard -- Lightweight OCR Mode.

Uses OCR (Tesseract or Windows native) to extract text from screenshots,
then runs the rule-based pre-screener against the extracted text.
No LLM needed. Runs on any device with minimal resources.

Only escalates to Gemma 4 when suspicious text is found AND the model
is available. This is the fallback for low-memory devices.

Usage:
    python -m guard.ocr_guard
    python -m guard.ocr_guard --interval 3
"""

import argparse
import base64
import io
import json
import logging
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from PIL import ImageGrab, Image
except ImportError:
    print("Install Pillow: pip install Pillow")
    sys.exit(1)

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

try:
    from win10toast import ToastNotifier
    _toaster = ToastNotifier()
except ImportError:
    _toaster = None

# ---- Configuration ----

CHECK_INTERVAL = 5
ALERT_THRESHOLD = 40  # Lower threshold since rules are less precise than LLM

LOG_DIR = Path(__file__).parent / "logs"
ALERT_LOG = Path(__file__).parent / "alert_history.json"

# ---- Scam Patterns (same as pre-screener, expanded for screen monitoring) ----

URGENCY_PATTERNS = [
    r"\b(act now|immediately|urgent|right away|don'?t delay)\b",
    r"\b(limited time|expires? (today|soon|in \d+))\b",
    r"\b(final (notice|warning|chance))\b",
    r"\b(within \d+ hours?|last chance)\b",
    r"\b(account.{0,20}(suspended|locked|closed|terminated|compromised))\b",
    r"\b(verify.{0,15}(immediately|now|today))\b",
]

AUTHORITY_PATTERNS = [
    r"\b(irs|social security|ssa|fbi|police|sheriff|department of)\b",
    r"\b(apple.{0,5}(id|security)|microsoft.{0,5}(security|support|account))\b",
    r"\b(bank.{0,15}security|account.{0,15}(suspended|locked|compromised))\b",
    r"\b(warrant.{0,15}(arrest|issued))\b",
    r"\b(paypal|netflix|amazon).{0,15}(security|verify|suspended)\b",
]

PAYMENT_PATTERNS = [
    r"\b(gift card|itunes card|google play card|steam card)\b",
    r"\b(western union|moneygram|wire transfer|bitcoin|crypto)\b",
    r"\b(processing fee|advance fee|shipping fee)\b",
    r"\b(update.{0,10}payment|payment.{0,10}(details|method|information))\b",
    r"\b(credit card.{0,10}(number|expired|update))\b",
]

PHISHING_PATTERNS = [
    r"\b(click here|click below|click the link|tap here)\b",
    r"\b(verify your (identity|account|email|information))\b",
    r"\b(confirm your (identity|account|details|password))\b",
    r"\b(log.?in.{0,10}(now|here|below|immediately))\b",
    r"\b(update your (password|credentials|information|details))\b",
    r"\b(unusual (activity|sign.?in|login|access))\b",
    r"\b(unauthorized (access|activity|transaction))\b",
    r"\b(dear (user|customer|member|valued))\b",
]

SUSPICIOUS_URL_PATTERNS = [
    r"https?://[^\s]*\.(xyz|tk|ml|ga|cf|gq|top|club|work|buzz)\b",
    r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
    r"https?://[^\s]*-(verify|secure|login|confirm|update)[^\s]*",
    r"https?://[^\s]*(signin|log-in|account-verify)[^\s]*",
]

GREED_PATTERNS = [
    r"\b(you('ve)? (won|been selected|inherited))\b",
    r"\b(lottery|sweepstakes|jackpot|prize)\b",
    r"\b(million (dollars|usd|\$))\b",
    r"\b(congratulations!?|winner!?)\b",
    r"\b(free (money|gift|iphone|prize))\b",
]

# ---- Logging ----

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [OCR-Guard] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("ocr-guard")


# ---- OCR ----

def extract_text_from_screen() -> str:
    """Capture screen and extract text via OCR."""
    img = ImageGrab.grab()
    # Resize for faster OCR
    img = img.resize((1280, 720), Image.LANCZOS)

    if HAS_TESSERACT:
        try:
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            log.debug(f"Tesseract failed: {e}")

    # Fallback: use Windows OCR via PowerShell (Win10+)
    try:
        import subprocess
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        # Save temp file for PowerShell OCR
        tmp = Path(__file__).parent / "logs" / "_ocr_tmp.png"
        tmp.parent.mkdir(exist_ok=True)
        with open(tmp, "wb") as f:
            f.write(buf.getvalue())

        ps_cmd = f"""
        Add-Type -AssemblyName System.Runtime.WindowsRuntime
        $null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
        $null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime]
        $null = [Windows.Storage.StorageFile, Windows.Foundation, ContentType = WindowsRuntime]

        $file = [Windows.Storage.StorageFile]::GetFileFromPathAsync('{tmp.absolute()}').GetAwaiter().GetResult()
        $stream = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read).GetAwaiter().GetResult()
        $decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
        $bitmap = $decoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()
        $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
        $result = $engine.RecognizeAsync($bitmap).GetAwaiter().GetResult()
        Write-Output $result.Text
        """
        result = subprocess.run(
            ["powershell", "-Command", ps_cmd],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception as e:
        log.debug(f"Windows OCR failed: {e}")

    return ""


def image_hash(img: Image.Image) -> str:
    """Quick perceptual hash for change detection."""
    small = img.resize((16, 16), Image.LANCZOS).convert("L")
    pixels = list(small.getdata())
    avg = sum(pixels) / len(pixels)
    return "".join("1" if p > avg else "0" for p in pixels)


def screen_changed(hash1: str, hash2: str) -> bool:
    """Check if screen changed."""
    if not hash1 or not hash2:
        return True
    diff = sum(a != b for a, b in zip(hash1, hash2))
    return (diff / len(hash1)) * 100 >= 3


# ---- Analysis ----

def analyze_text(text: str) -> dict:
    """Run rule-based analysis on extracted text."""
    text_lower = text.lower()
    flags = []
    score_deductions = 0

    categories = [
        (URGENCY_PATTERNS, "Urgency/pressure language detected", 15),
        (AUTHORITY_PATTERNS, "Authority impersonation detected", 20),
        (PAYMENT_PATTERNS, "Suspicious payment request detected", 20),
        (PHISHING_PATTERNS, "Phishing indicators detected", 20),
        (SUSPICIOUS_URL_PATTERNS, "Suspicious URL detected", 25),
        (GREED_PATTERNS, "Too-good-to-be-true offer detected", 15),
    ]

    matched_details = []
    for patterns, flag_name, deduction in categories:
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                flags.append(flag_name)
                matched_details.append(match.group(0))
                score_deductions += deduction
                break

    threat_score = max(0, 100 - score_deductions)
    threat_detected = len(flags) >= 2  # Need at least 2 categories to flag

    return {
        "threat_detected": threat_detected,
        "confidence": min(100, score_deductions),
        "threat_type": "phishing" if any("phish" in f.lower() for f in flags) else "scam" if flags else "none",
        "severity": "critical" if score_deductions >= 60 else "high" if score_deductions >= 40 else "medium" if score_deductions >= 20 else "none",
        "flags": flags,
        "matched_text": matched_details,
        "description": f"Detected {len(flags)} suspicious patterns: {', '.join(flags[:3])}" if flags else "No threats detected",
        "recommendation": "Do not click any links or provide personal information. Close this page." if threat_detected else "",
        "trust_score": threat_score,
    }


# ---- Notification ----

def send_alert(result: dict):
    """Send Windows notification."""
    title = f"Beacon Guard -- {result.get('severity', 'HIGH').upper()} THREAT"
    message = result.get("description", "Suspicious activity detected")

    log.warning(f"ALERT: {title} -- {message}")

    if _toaster:
        try:
            _toaster.show_toast(title, message, duration=10, threaded=True)
        except Exception:
            pass


def save_alert(result: dict):
    """Save to local alert history."""
    history = []
    if ALERT_LOG.exists():
        try:
            history = json.loads(ALERT_LOG.read_text())
        except Exception:
            pass
    history.append({"timestamp": datetime.now().isoformat(), **result})
    history = history[-100:]
    ALERT_LOG.write_text(json.dumps(history, indent=2))


# ---- Main Loop ----

def run_guard(interval: int = CHECK_INTERVAL, threshold: int = ALERT_THRESHOLD):
    log.info("=" * 50)
    log.info("Beacon Guard -- OCR Mode (Lightweight)")
    log.info(f"Check interval: {interval}s")
    log.info(f"Alert threshold: {threshold}% confidence")
    log.info(f"OCR engine: {'Tesseract' if HAS_TESSERACT else 'Windows Native / Fallback'}")
    log.info("No LLM required. Runs on any device.")
    log.info("=" * 50)
    log.info("")

    LOG_DIR.mkdir(exist_ok=True)
    last_hash = ""
    checks = 0
    alerts = 0

    while True:
        try:
            # Capture and check for change
            img = ImageGrab.grab()
            current_hash = image_hash(img)

            if not screen_changed(last_hash, current_hash):
                time.sleep(interval)
                continue

            last_hash = current_hash
            checks += 1

            # Extract text via OCR
            text = extract_text_from_screen()
            if not text or len(text.strip()) < 20:
                log.info(f"Check #{checks}: No readable text on screen")
                time.sleep(interval)
                continue

            # Analyze extracted text
            result = analyze_text(text)
            threat = result.get("threat_detected", False)
            confidence = result.get("confidence", 0)

            if threat and confidence >= threshold:
                alerts += 1
                log.warning(f"THREAT (confidence: {confidence}%, flags: {len(result['flags'])})")
                for f in result["flags"]:
                    log.warning(f"  - {f}")
                for m in result["matched_text"]:
                    log.warning(f"    matched: \"{m}\"")
                send_alert(result)
                save_alert(result)
            else:
                log.info(f"Check #{checks}: Clean ({len(text)} chars extracted, {len(result.get('flags', []))} flags)")

        except KeyboardInterrupt:
            log.info(f"\nGuard stopped. {checks} checks, {alerts} alerts.")
            break
        except Exception as e:
            log.error(f"Error: {e}")

        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Beacon Guard -- OCR Lightweight Mode")
    parser.add_argument("--interval", type=int, default=CHECK_INTERVAL)
    parser.add_argument("--threshold", type=int, default=ALERT_THRESHOLD)
    args = parser.parse_args()
    run_guard(interval=args.interval, threshold=args.threshold)
