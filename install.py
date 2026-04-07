"""Beacon -- Fully Automated One-Click Installer.

Installs EVERYTHING automatically. No user input needed except
one optional prompt for startup. Downloads and installs Ollama,
pulls Gemma 4, installs all Python deps, creates launchers.

Usage:
    python install.py           # Full automated install
    python install.py --silent  # No prompts at all
"""

import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request


OLLAMA_WINDOWS_URL = "https://ollama.com/download/OllamaSetup.exe"
OLLAMA_MAC_URL = "https://ollama.com/download/Ollama-darwin.zip"
OLLAMA_LINUX_CMD = "curl -fsSL https://ollama.com/install.sh | sh"

SILENT = "--silent" in sys.argv


def print_banner():
    print()
    print("=" * 55)
    print("  BEACON INSTALLER")
    print("  Privacy-First AI Protection for Everyone")
    print("  Fully Automated -- Sit Back and Relax")
    print("=" * 55)
    print()


def check_python():
    v = sys.version_info
    print(f"[1/6] Python {v.major}.{v.minor}.{v.micro}")
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        print("      Python 3.10+ required. Please upgrade.")
        sys.exit(1)
    print("      OK")


def install_ollama():
    """Download and install Ollama automatically if not present."""
    print("[2/6] Checking Ollama...")

    if shutil.which("ollama"):
        print("      Ollama already installed")
        return True

    system = platform.system()
    print("      Ollama not found -- installing automatically...")

    try:
        if system == "Windows":
            # Download Ollama installer
            installer_path = os.path.join(tempfile.gettempdir(), "OllamaSetup.exe")
            print(f"      Downloading Ollama installer...")
            urllib.request.urlretrieve(OLLAMA_WINDOWS_URL, installer_path)
            print(f"      Downloaded to {installer_path}")

            # Run installer silently
            print("      Running Ollama installer (this may take a minute)...")
            subprocess.run([installer_path, "/VERYSILENT", "/NORESTART"], check=True)
            print("      Ollama installed successfully")

            # Ollama may need a moment to register in PATH
            # Try to find it in common locations
            ollama_paths = [
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Ollama", "ollama.exe"),
                os.path.join(os.environ.get("PROGRAMFILES", ""), "Ollama", "ollama.exe"),
                shutil.which("ollama"),
            ]
            for p in ollama_paths:
                if p and os.path.exists(p):
                    # Add to PATH for this session
                    os.environ["PATH"] = os.path.dirname(p) + os.pathsep + os.environ["PATH"]
                    print(f"      Found at: {p}")
                    break

            return True

        elif system == "Darwin":
            print("      Downloading Ollama for macOS...")
            zip_path = os.path.join(tempfile.gettempdir(), "Ollama-darwin.zip")
            urllib.request.urlretrieve(OLLAMA_MAC_URL, zip_path)
            subprocess.run(["unzip", "-o", zip_path, "-d", "/Applications"], check=True)
            print("      Ollama installed to /Applications")
            return True

        elif system == "Linux":
            print("      Installing Ollama via official script...")
            subprocess.run(["bash", "-c", OLLAMA_LINUX_CMD], check=True)
            print("      Ollama installed")
            return True

    except Exception as e:
        print(f"      Auto-install failed: {e}")
        print()
        print("      Please install Ollama manually:")
        print("      https://ollama.com/download")
        print()
        if SILENT:
            return False
        resp = input("      Continue without Ollama? (y/n): ").strip().lower()
        return resp == "y"

    return False


def start_ollama():
    """Make sure Ollama service is running."""
    print("[3/6] Starting Ollama service...")
    try:
        import httpx
        r = httpx.get("http://localhost:11434/api/tags", timeout=3)
        if r.status_code == 200:
            print("      Ollama is running")
            return True
    except Exception:
        pass

    # Try to start Ollama
    system = platform.system()
    try:
        if system == "Windows":
            # Find ollama.exe
            ollama_exe = shutil.which("ollama")
            if not ollama_exe:
                for p in [
                    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Ollama", "ollama.exe"),
                    os.path.join(os.environ.get("PROGRAMFILES", ""), "Ollama", "ollama.exe"),
                ]:
                    if os.path.exists(p):
                        ollama_exe = p
                        break

            if ollama_exe:
                subprocess.Popen(
                    [ollama_exe, "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW if system == "Windows" else 0,
                )
                import time
                time.sleep(3)
                print("      Ollama started")
                return True
        else:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            import time
            time.sleep(3)
            print("      Ollama started")
            return True
    except Exception as e:
        print(f"      Could not start Ollama: {e}")
        print("      Start Ollama manually, then run install.py again")

    return False


def install_deps():
    print("[4/6] Installing Python dependencies...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt",
        "--quiet",
    ])

    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", "guard/requirements.txt",
        "--quiet",
    ])

    if platform.system() == "Windows":
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "win10toast", "--quiet",
        ])

    print("      All dependencies installed")


def pull_gemma():
    print("[5/6] Pulling Gemma 4 model (~9.6 GB, one-time download)...")
    print("      This may take several minutes on first install.")
    try:
        subprocess.check_call(["ollama", "pull", "gemma4:e4b"])
        print("      Gemma 4 E4B ready")
        return True
    except FileNotFoundError:
        print("      Skipped (Ollama not in PATH)")
        return False
    except subprocess.CalledProcessError:
        print("      Failed. Make sure Ollama is running, then run:")
        print("      ollama pull gemma4:e4b")
        return False


def create_shortcuts():
    print("[6/6] Creating launchers...")
    system = platform.system()
    beacon_dir = os.path.abspath(".")
    python = sys.executable

    if system == "Windows":
        # All-in-one launcher (web app + guard + opens browser)
        with open("Beacon.bat", "w") as f:
            f.write('@echo off\n')
            f.write(f'cd /d "{beacon_dir}"\n')
            f.write('echo.\n')
            f.write('echo ================================================\n')
            f.write('echo   BEACON -- AI-Powered Protection for Everyone\n')
            f.write('echo ================================================\n')
            f.write('echo.\n')
            f.write('echo Starting Beacon + Guard...\n')
            f.write('echo Browser will open automatically.\n')
            f.write('echo.\n')
            f.write(f'"{python}" beacon_app.py\n')
            f.write('pause\n')
        print("      Created: Beacon.bat (all-in-one launcher)")

        # Standalone launchers
        with open("Start Beacon.bat", "w") as f:
            f.write(f'@echo off\ncd /d "{beacon_dir}"\n"{python}" run.py\npause\n')
        with open("Start Guard.bat", "w") as f:
            f.write(f'@echo off\ncd /d "{beacon_dir}"\necho Beacon Guard running silently...\n"{python}" -m guard.beacon_guard\npause\n')
        with open("Start Guard Monitor.bat", "w") as f:
            f.write(f'@echo off\ncd /d "{beacon_dir}"\necho Guard Monitor: http://localhost:8001\n"{python}" -m guard.monitor\npause\n')
        print("      Created: Start Beacon.bat, Start Guard.bat, Start Guard Monitor.bat")

        # Auto-start Guard on login
        if SILENT:
            add_startup = True
        else:
            print()
            resp = input("      Start Beacon Guard automatically on login? (y/n): ").strip().lower()
            add_startup = resp == "y"

        if add_startup:
            try:
                startup_dir = os.path.join(
                    os.environ.get("APPDATA", ""),
                    "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
                )
                shortcut_path = os.path.join(startup_dir, "Beacon Guard.bat")
                with open(shortcut_path, "w") as f:
                    f.write('@echo off\n')
                    f.write(f'cd /d "{beacon_dir}"\n')
                    f.write(f'start /min "" "{python}" -m guard.beacon_guard\n')
                print(f"      Guard added to Windows startup")
            except Exception as e:
                print(f"      Could not add to startup: {e}")

    else:
        for name, cmd in [
            ("beacon.sh", f'#!/bin/bash\ncd "$(dirname "$0")"\n{python} beacon_app.py'),
            ("start_beacon.sh", f'#!/bin/bash\ncd "$(dirname "$0")"\n{python} run.py'),
            ("start_guard.sh", f'#!/bin/bash\ncd "$(dirname "$0")"\n{python} -m guard.beacon_guard'),
            ("start_monitor.sh", f'#!/bin/bash\ncd "$(dirname "$0")"\n{python} -m guard.monitor'),
        ]:
            with open(name, "w") as f:
                f.write(cmd + "\n")
            os.chmod(name, 0o755)
        print("      Created: beacon.sh, start_beacon.sh, start_guard.sh, start_monitor.sh")


def print_summary():
    print()
    print("=" * 55)
    print("  INSTALLATION COMPLETE")
    print("=" * 55)
    print()
    if platform.system() == "Windows":
        print('  Double-click "Beacon.bat" to start everything.')
    else:
        print("  Run ./beacon.sh to start everything.")
    print()
    print("  What happens:")
    print("  - Beacon web app opens at http://localhost:8000")
    print("  - Beacon Guard monitors your screen silently")
    print("  - You get a notification if a threat is detected")
    print()
    print("  All AI runs locally. No data ever leaves your device.")
    print()


def main():
    print_banner()
    check_python()
    install_ollama()
    start_ollama()
    install_deps()
    pull_gemma()
    create_shortcuts()
    print_summary()


if __name__ == "__main__":
    main()
