"""Beacon -- Single Entry Point for PyInstaller packaging.

This file launches both the Beacon web app and Beacon Guard simultaneously.
When packaged as an .exe, the user double-clicks one file and everything runs.
"""

import multiprocessing
import os
import subprocess
import sys
import threading
import time
import webbrowser


def start_beacon_server():
    """Start the FastAPI web app."""
    import uvicorn
    from backend.main import app
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")


def start_guard():
    """Start Beacon Guard in background."""
    time.sleep(5)  # Let server start first
    try:
        from guard.beacon_guard import run_guard
        run_guard(interval=10, threshold=85, change_pct=5)
    except Exception as e:
        print(f"Guard error: {e}")


def check_ollama():
    """Check if Ollama is running and has Gemma 4."""
    try:
        import httpx
        r = httpx.get("http://localhost:11434/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        if any("gemma4" in m for m in models):
            return True
        print()
        print("Gemma 4 model not found. Pulling now...")
        print("This is a one-time ~9.6 GB download.")
        print()
        subprocess.run(["ollama", "pull", "gemma4:e4b"], check=True)
        return True
    except Exception:
        return False


def main():
    print()
    print("=" * 50)
    print("  BEACON -- AI-Powered Protection for Everyone")
    print("=" * 50)
    print()

    # Check Ollama
    if not check_ollama():
        print("Ollama is not running or not installed.")
        print()
        print("Beacon needs Ollama for AI features.")
        print("Download free: https://ollama.com/download")
        print()
        print("Quick Scan (rule-based) will still work without Ollama.")
        print()

    print("Starting Beacon web app on http://localhost:8000")
    print("Starting Beacon Guard (silent background protection)")
    print()
    print("Opening browser...")
    print("Press Ctrl+C to stop everything.")
    print()

    # Open browser after a short delay
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://localhost:8000")

    threading.Thread(target=open_browser, daemon=True).start()

    # Start Guard in background thread
    guard_thread = threading.Thread(target=start_guard, daemon=True)
    guard_thread.start()

    # Start server in main thread (blocks)
    try:
        start_beacon_server()
    except KeyboardInterrupt:
        print("\nBeacon stopped.")


if __name__ == "__main__":
    multiprocessing.freeze_support()  # Required for PyInstaller
    main()
