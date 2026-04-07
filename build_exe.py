"""Build Beacon into a standalone .exe installer.

Usage:
    python build_exe.py

Output:
    dist/Beacon/Beacon.exe  -- standalone executable (run this)
    dist/Beacon/            -- full directory with all dependencies

The user just needs:
    1. Ollama installed (https://ollama.com/download)
    2. Double-click Beacon.exe

Everything else is bundled.
"""

import subprocess
import sys
import shutil
from pathlib import Path


def build():
    print("=" * 50)
    print("  Building Beacon Executable")
    print("=" * 50)
    print()

    # Clean previous builds
    for d in ["build", "dist"]:
        if Path(d).exists():
            shutil.rmtree(d)
            print(f"Cleaned {d}/")

    # Run PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "Beacon",
        "--onedir",              # Directory mode (faster startup than --onefile)
        "--console",             # Show console for Guard logs
        "--noconfirm",
        # Add data files
        "--add-data", "frontend;frontend",
        "--add-data", "backend/prompts;backend/prompts",
        "--add-data", "training/data;training/data",
        "--add-data", "guard;guard",
        # Hidden imports that PyInstaller might miss
        "--hidden-import", "uvicorn.logging",
        "--hidden-import", "uvicorn.loops",
        "--hidden-import", "uvicorn.loops.auto",
        "--hidden-import", "uvicorn.protocols",
        "--hidden-import", "uvicorn.protocols.http",
        "--hidden-import", "uvicorn.protocols.http.auto",
        "--hidden-import", "uvicorn.protocols.websockets",
        "--hidden-import", "uvicorn.protocols.websockets.auto",
        "--hidden-import", "uvicorn.lifespan",
        "--hidden-import", "uvicorn.lifespan.on",
        "--hidden-import", "backend",
        "--hidden-import", "backend.main",
        "--hidden-import", "backend.routers",
        "--hidden-import", "backend.routers.scanner",
        "--hidden-import", "backend.routers.contracts",
        "--hidden-import", "backend.routers.rights",
        "--hidden-import", "backend.routers.streaming",
        "--hidden-import", "backend.routers.alerts",
        "--hidden-import", "backend.services",
        "--hidden-import", "backend.services.scam_analyzer",
        "--hidden-import", "backend.services.contract_analyzer",
        "--hidden-import", "backend.services.rights_navigator",
        "--hidden-import", "backend.services.prescreener",
        "--hidden-import", "backend.services.alert_service",
        "--hidden-import", "backend.ollama_client",
        "--hidden-import", "backend.config",
        "--hidden-import", "guard.beacon_guard",
        "--hidden-import", "win10toast",
        "--hidden-import", "PIL",
        "--hidden-import", "psutil",
        "--hidden-import", "plyer.platforms.win.notification",
        # Entry point
        "beacon_app.py",
    ]

    print("Running PyInstaller...")
    print()
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print()
        print("=" * 50)
        print("  BUILD SUCCESSFUL")
        print("=" * 50)
        print()
        print("  Output: dist/Beacon/Beacon.exe")
        print()
        print("  To distribute:")
        print("  1. Zip the dist/Beacon/ folder")
        print("  2. Share the zip file")
        print("  3. User unzips and double-clicks Beacon.exe")
        print("  4. (User needs Ollama installed separately)")
        print()
        print("  Or use an installer tool like NSIS or Inno Setup")
        print("  to create a proper Setup.exe from the dist/Beacon/ folder.")
    else:
        print()
        print("BUILD FAILED. Check errors above.")
        sys.exit(1)


if __name__ == "__main__":
    build()
