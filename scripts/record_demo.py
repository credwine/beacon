"""
Beacon Hackathon Demo Recorder
================================
Records a polished, rehearsed walkthrough of the Beacon app using Playwright.
The app must be running at http://localhost:8000 before executing this script.

Usage:
    pip install playwright
    python -m playwright install chromium
    python scripts/record_demo.py

Output:
    scripts/demo_recording.webm
"""

import os
import sys
import time
import random
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

APP_URL = "http://localhost:8000"
VIEWPORT = {"width": 1920, "height": 1080}
SCRIPT_DIR = Path(__file__).resolve().parent
VIDEO_DIR = SCRIPT_DIR / "tmp_video"
OUTPUT_FILE = SCRIPT_DIR / "demo_recording.webm"

# The scam email used for the Deep Scan step
DEEP_SCAN_EMAIL = (
    "URGENT: Your Apple ID has been compromised! Click here immediately to "
    "verify your identity: http://apple-secure-verify.xyz/login. You have 24 "
    "hours before your account is permanently deleted. Apple Security Team "
    "Case #APL-2024-889271"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def human_delay(low: float = 0.4, high: float = 1.0) -> None:
    """Sleep for a realistic human-like pause between actions."""
    time.sleep(random.uniform(low, high))


def slow_type(page, selector: str, text: str, delay_low: int = 30, delay_high: int = 80) -> None:
    """Type text character by character with small random delays (ms)."""
    el = page.locator(selector)
    el.click()
    for ch in text:
        el.type(ch, delay=0)
        time.sleep(random.randint(delay_low, delay_high) / 1000.0)


def wait_and_click(page, selector: str, timeout: int = 10000) -> None:
    """Wait for an element to be visible, then click it."""
    page.locator(selector).wait_for(state="visible", timeout=timeout)
    human_delay(0.3, 0.6)
    page.locator(selector).click()


def step(msg: str) -> None:
    """Print a timestamped progress message."""
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}]  {msg}")


# ---------------------------------------------------------------------------
# Demo Script
# ---------------------------------------------------------------------------


def run_demo():
    step("Starting Playwright")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)

        # Ensure temp video dir exists and is clean
        if VIDEO_DIR.exists():
            shutil.rmtree(VIDEO_DIR)
        VIDEO_DIR.mkdir(parents=True)

        context = browser.new_context(
            viewport=VIEWPORT,
            record_video_dir=str(VIDEO_DIR),
            record_video_size=VIEWPORT,
            color_scheme="light",
        )

        page = context.new_page()

        # ------------------------------------------------------------------
        # 1. Landing page -- let the animated demo play
        # ------------------------------------------------------------------
        step("1/12  Opening landing page")
        page.goto(APP_URL, wait_until="networkidle")
        # Give the hero demo animation time to type and show results
        page.wait_for_timeout(6000)
        step("       Landing animation observed")

        # ------------------------------------------------------------------
        # 2. Click "Start Protecting Yourself" to launch the app
        # ------------------------------------------------------------------
        step("2/12  Clicking 'Start Protecting Yourself'")
        human_delay(0.8, 1.2)
        # This is the big CTA button in the hero
        page.locator("button.btn-primary.btn-lg", has_text="Start Protecting Yourself").click()
        page.wait_for_selector("#app", state="visible", timeout=5000)
        page.wait_for_timeout(1000)
        step("       App launched")

        # ------------------------------------------------------------------
        # 3. Toggle dark mode (click moon icon in app nav)
        # ------------------------------------------------------------------
        step("3/12  Toggling dark mode ON")
        human_delay(0.6, 1.0)
        # The app nav theme toggle button (second one on page, inside #app)
        theme_btn = page.locator("#app .theme-toggle")
        theme_btn.click()
        page.wait_for_timeout(1500)
        step("       Dark mode active")

        # Toggle back to light for the rest of the demo
        step("       Toggling dark mode OFF")
        human_delay(0.5, 0.8)
        theme_btn.click()
        page.wait_for_timeout(1000)
        step("       Light mode restored")

        # ------------------------------------------------------------------
        # 4. Switch language to Spanish, then back to English
        # ------------------------------------------------------------------
        step("4/12  Switching language to Spanish")
        human_delay(0.5, 0.8)
        page.select_option("#languageSelector", "es")
        page.wait_for_timeout(2000)
        step("       UI now in Spanish")

        human_delay(0.5, 0.8)
        step("       Switching back to English")
        page.select_option("#languageSelector", "en")
        page.wait_for_timeout(1000)
        step("       English restored")

        # ------------------------------------------------------------------
        # 5. Scam Scanner -- Try Example + Quick Scan
        # ------------------------------------------------------------------
        step("5/12  Scam Scanner: clicking 'Try Example'")
        human_delay(0.5, 0.8)
        # The "Try Example" button in the scanner panel
        page.locator("#panel-scanner button", has_text="Try Example").click()
        page.wait_for_timeout(1000)
        step("       Example loaded")

        step("       Clicking 'Quick Scan'")
        human_delay(0.4, 0.7)
        page.locator("#quickScanBtn").click()
        # Quick Scan is instant (rule-based), but wait for result to render
        page.wait_for_selector("#scanResult .trust-score-display", state="visible", timeout=10000)
        page.wait_for_timeout(2500)
        step("       Quick Scan results displayed")

        # ------------------------------------------------------------------
        # 6. Clear, paste a different scam, and click Deep Scan
        # ------------------------------------------------------------------
        step("6/12  Clearing scanner")
        human_delay(0.5, 0.8)
        page.locator("#panel-scanner button", has_text="Clear").click()
        page.wait_for_timeout(800)
        step("       Scanner cleared")

        step("       Typing scam email for Deep Scan")
        human_delay(0.3, 0.6)
        slow_type(page, "#scanInput", DEEP_SCAN_EMAIL, delay_low=18, delay_high=45)
        page.wait_for_timeout(500)
        step("       Scam email typed")

        step("       Clicking 'Deep Scan'")
        human_delay(0.4, 0.7)
        page.locator("#scanBtn").click()
        step("       Deep Scan started -- waiting for AI results...")

        # ------------------------------------------------------------------
        # 7. Wait for streaming Deep Scan results
        # ------------------------------------------------------------------
        # Deep Scan calls the LLM and can take 30-60 seconds
        page.wait_for_selector(
            "#scanResult .trust-score-ring, #scanResult .trust-score-display",
            state="visible",
            timeout=90000
        )
        # Give a bit more time for the full result to render (explanation, red flags, etc.)
        page.wait_for_timeout(3000)
        step("7/12  Deep Scan results visible (trust score, red flags, explanation)")

        # Scroll the result side to show all content
        page.locator("#scanResult").evaluate("el => el.scrollTop = el.scrollHeight")
        page.wait_for_timeout(2000)
        # Scroll back to top
        page.locator("#scanResult").evaluate("el => el.scrollTop = 0")
        page.wait_for_timeout(1000)

        # ------------------------------------------------------------------
        # 8. Switch to Contract Reader -- Try Example + Analyze
        # ------------------------------------------------------------------
        step("8/12  Switching to Contract Reader tab")
        human_delay(0.5, 0.8)
        page.locator(".tab[data-tab='contracts']").click()
        page.wait_for_selector("#panel-contracts.active", state="visible", timeout=5000)
        page.wait_for_timeout(800)

        step("       Clicking 'Try Example'")
        human_delay(0.4, 0.7)
        page.locator("#panel-contracts button", has_text="Try Example").click()
        page.wait_for_timeout(1000)
        step("       Contract example loaded")

        step("       Clicking 'Analyze Document'")
        human_delay(0.4, 0.7)
        page.locator("#contractBtn").click()
        step("       Contract analysis started -- waiting for AI results...")

        # ------------------------------------------------------------------
        # 9. Wait for contract analysis results
        # ------------------------------------------------------------------
        page.wait_for_selector(
            "#contractResult .result-section",
            state="visible",
            timeout=90000
        )
        page.wait_for_timeout(3000)
        step("9/12  Contract analysis results displayed")

        # Scroll through results
        page.locator("#contractResult").evaluate("el => el.scrollTop = el.scrollHeight")
        page.wait_for_timeout(2000)
        page.locator("#contractResult").evaluate("el => el.scrollTop = 0")
        page.wait_for_timeout(1000)

        # ------------------------------------------------------------------
        # 10. Switch to Settings tab -- show Trusted Contacts form
        # ------------------------------------------------------------------
        step("10/12 Switching to Settings tab")
        human_delay(0.5, 0.8)
        page.locator(".tab[data-tab='settings']").click()
        page.wait_for_selector("#panel-settings.active", state="visible", timeout=5000)
        page.wait_for_timeout(1500)
        step("       Settings / Trusted Contacts form visible")

        # Slowly scroll down to show the entire settings page
        page.evaluate("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })")
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
        page.wait_for_timeout(1500)

        # ------------------------------------------------------------------
        # 11. Open history drawer (clock icon)
        # ------------------------------------------------------------------
        step("11/12 Opening history drawer")
        human_delay(0.5, 0.8)
        page.locator(".history-toggle-btn").click()
        page.wait_for_selector("#historyDrawer.open", state="visible", timeout=5000)
        page.wait_for_timeout(2500)
        step("       History drawer open -- showing past analyses")

        # ------------------------------------------------------------------
        # 12. Close history drawer
        # ------------------------------------------------------------------
        step("12/12 Closing history drawer")
        human_delay(0.5, 0.8)
        # Click the X button inside the drawer header
        page.locator("#historyDrawer .history-drawer-header button").click()
        page.wait_for_timeout(1500)
        step("       History drawer closed")

        # Final pause so the video has a clean ending
        page.wait_for_timeout(2000)

        # ------------------------------------------------------------------
        # Save recording
        # ------------------------------------------------------------------
        step("Closing browser and saving video...")
        page.close()
        context.close()
        browser.close()

        # Move the recording to the expected output path
        video_files = list(VIDEO_DIR.glob("*.webm"))
        if not video_files:
            print("ERROR: No video file was produced. Check Playwright video recording support.")
            sys.exit(1)

        # Take the first (and usually only) video file
        src = video_files[0]
        shutil.move(str(src), str(OUTPUT_FILE))

        # Clean up temp dir
        shutil.rmtree(VIDEO_DIR, ignore_errors=True)

        step(f"Demo recording saved to: {OUTPUT_FILE}")
        print(f"\n  {OUTPUT_FILE}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_demo()
