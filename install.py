"""Beacon -- One-Click Installer.

Sets up everything a user needs to run Beacon + Beacon Guard.
Works on Windows, macOS, and Linux.

Usage:
    python install.py
"""

import os
import platform
import shutil
import subprocess
import sys


def print_banner():
    print()
    print("=" * 55)
    print("  BEACON INSTALLER")
    print("  Privacy-First AI Protection for Everyone")
    print("=" * 55)
    print()


def check_python():
    v = sys.version_info
    print(f"[+] Python {v.major}.{v.minor}.{v.micro}")
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        print("[!] Python 3.10+ required. Please upgrade.")
        sys.exit(1)
    print("    OK")


def check_ollama():
    print("[+] Checking Ollama...")
    if shutil.which("ollama"):
        print("    Ollama found")
        return True
    else:
        print("    Ollama not found")
        print()
        print("    Ollama is required for Beacon's AI features.")
        print("    Download it free from: https://ollama.com/download")
        print()
        resp = input("    Continue without Ollama? (y/n): ").strip().lower()
        return resp == "y"


def install_deps():
    print("[+] Installing Beacon dependencies...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt",
        "--quiet",
    ])
    print("    Core dependencies installed")

    print("[+] Installing Beacon Guard dependencies...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", "guard/requirements.txt",
        "--quiet",
    ])
    # Windows-specific notification library
    if platform.system() == "Windows":
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "win10toast", "--quiet",
        ])
    print("    Guard dependencies installed")


def pull_gemma():
    print("[+] Pulling Gemma 4 model (one-time download, ~9.6 GB)...")
    print("    This may take several minutes on first install.")
    try:
        subprocess.check_call(["ollama", "pull", "gemma4:e4b"])
        print("    Gemma 4 E4B ready")
    except FileNotFoundError:
        print("    Skipped (Ollama not installed)")
    except subprocess.CalledProcessError:
        print("    Failed. Make sure Ollama is running, then run:")
        print("    ollama pull gemma4:e4b")


def create_shortcuts():
    system = platform.system()

    if system == "Windows":
        print("[+] Creating start scripts...")

        # Beacon web app launcher
        with open("Start Beacon.bat", "w") as f:
            f.write('@echo off\n')
            f.write('echo Starting Beacon...\n')
            f.write('echo Open http://localhost:8000 in your browser\n')
            f.write(f'"{sys.executable}" run.py\n')
            f.write('pause\n')
        print("    Created: Start Beacon.bat")

        # Guard launcher
        with open("Start Guard.bat", "w") as f:
            f.write('@echo off\n')
            f.write('echo Starting Beacon Guard (silent mode)...\n')
            f.write('echo Guard is now monitoring your screen.\n')
            f.write('echo You will only see notifications if a threat is detected.\n')
            f.write('echo Press Ctrl+C to stop.\n')
            f.write(f'"{sys.executable}" -m guard.beacon_guard\n')
            f.write('pause\n')
        print("    Created: Start Guard.bat")

        # Guard monitor launcher
        with open("Start Guard Monitor.bat", "w") as f:
            f.write('@echo off\n')
            f.write('echo Starting Beacon Guard Monitor Dashboard...\n')
            f.write('echo Open http://localhost:8001 in your browser\n')
            f.write(f'"{sys.executable}" -m guard.monitor\n')
            f.write('pause\n')
        print("    Created: Start Guard Monitor.bat")

        # Add Guard to Windows startup (optional)
        print()
        resp = input("    Add Beacon Guard to Windows startup? (y/n): ").strip().lower()
        if resp == "y":
            try:
                startup_dir = os.path.join(
                    os.environ.get("APPDATA", ""),
                    "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
                )
                shortcut_path = os.path.join(startup_dir, "Beacon Guard.bat")
                beacon_dir = os.path.abspath(".")
                with open(shortcut_path, "w") as f:
                    f.write('@echo off\n')
                    f.write(f'cd /d "{beacon_dir}"\n')
                    f.write(f'start /min "" "{sys.executable}" -m guard.beacon_guard\n')
                print(f"    Added to startup: {shortcut_path}")
                print("    Beacon Guard will start automatically when you log in.")
            except Exception as e:
                print(f"    Could not add to startup: {e}")
                print("    You can manually copy 'Start Guard.bat' to your Startup folder.")

    else:
        # macOS / Linux
        print("[+] Creating start scripts...")
        for name, cmd in [
            ("start_beacon.sh", f'#!/bin/bash\ncd "$(dirname "$0")"\n{sys.executable} run.py'),
            ("start_guard.sh", f'#!/bin/bash\ncd "$(dirname "$0")"\n{sys.executable} -m guard.beacon_guard'),
            ("start_monitor.sh", f'#!/bin/bash\ncd "$(dirname "$0")"\n{sys.executable} -m guard.monitor'),
        ]:
            with open(name, "w") as f:
                f.write(cmd + "\n")
            os.chmod(name, 0o755)
            print(f"    Created: {name}")


def print_summary():
    print()
    print("=" * 55)
    print("  INSTALLATION COMPLETE")
    print("=" * 55)
    print()
    print("  How to use Beacon:")
    print()
    print("  1. BEACON WEB APP (scan messages, contracts, rights)")
    if platform.system() == "Windows":
        print('     Double-click "Start Beacon.bat"')
    else:
        print("     ./start_beacon.sh")
    print("     Open http://localhost:8000")
    print()
    print("  2. BEACON GUARD (silent background protection)")
    if platform.system() == "Windows":
        print('     Double-click "Start Guard.bat"')
    else:
        print("     ./start_guard.sh")
    print("     Runs invisibly. Notifies you only when threats are found.")
    print()
    print("  3. GUARD MONITOR (live dashboard for demo)")
    if platform.system() == "Windows":
        print('     Double-click "Start Guard Monitor.bat"')
    else:
        print("     ./start_monitor.sh")
    print("     Open http://localhost:8001")
    print()
    print("  All AI runs locally. No data ever leaves your device.")
    print()


def main():
    print_banner()
    check_python()
    has_ollama = check_ollama()
    install_deps()
    if has_ollama:
        pull_gemma()
    create_shortcuts()
    print_summary()


if __name__ == "__main__":
    main()
