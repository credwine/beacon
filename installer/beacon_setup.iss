; Beacon -- Inno Setup Installer Script
; Creates a professional Windows Setup.exe
;
; Prerequisites:
;   1. Run: python build_exe.py (creates dist/Beacon/)
;   2. Install Inno Setup: https://jrsoftware.org/isdl.php
;   3. Open this file in Inno Setup Compiler and click Build
;
; Output: installer/BeaconSetup.exe

[Setup]
AppName=Beacon
AppVersion=1.0.0
AppPublisher=Forge Dev.studio
AppPublisherURL=https://forgedev.studio
AppSupportURL=https://github.com/credwine/beacon
DefaultDirName={autopf}\Beacon
DefaultGroupName=Beacon
OutputDir=.
OutputBaseFilename=BeaconSetup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
UninstallDisplayName=Beacon

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"
Name: "startupguard"; Description: "Start Beacon Guard on Windows startup (silent protection)"; GroupDescription: "Background protection:"

[Files]
; Bundle everything from PyInstaller output
Source: "..\dist\Beacon\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
; Start menu shortcuts
Name: "{group}\Beacon"; Filename: "{app}\Beacon.exe"; Comment: "AI-Powered Protection for Everyone"
Name: "{group}\Uninstall Beacon"; Filename: "{uninstallexe}"

; Desktop shortcut (optional)
Name: "{autodesktop}\Beacon"; Filename: "{app}\Beacon.exe"; Tasks: desktopicon; Comment: "AI-Powered Protection for Everyone"

; Startup shortcut for Guard (optional)
Name: "{userstartup}\Beacon Guard"; Filename: "{app}\Beacon.exe"; Parameters: "--guard-only"; Tasks: startupguard

[Run]
; Launch after install
Filename: "{app}\Beacon.exe"; Description: "Launch Beacon now"; Flags: postinstall nowait skipifsilent

[Messages]
WelcomeLabel1=Welcome to Beacon
WelcomeLabel2=Beacon is a free, privacy-first AI tool that protects you from scams, explains contracts in plain English, and helps you know your rights.%n%nAll AI runs locally on your device. No data ever leaves your computer.%n%nNote: Beacon requires Ollama (free) for AI features. Download it at ollama.com/download if you haven't already.
FinishedLabel=Beacon has been installed.%n%nDouble-click the Beacon icon to start. The app will open in your browser at http://localhost:8000.%n%nBeacon Guard runs silently in the background, monitoring your screen for threats.
