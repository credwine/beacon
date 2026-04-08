; Beacon -- Inno Setup Installer Script
; Creates a professional Windows Setup.exe that installs EVERYTHING
;
; Prerequisites:
;   1. Run: python build_exe.py (creates dist/Beacon/)
;   2. Download OllamaSetup.exe to installer/ folder
;   3. Install Inno Setup: https://jrsoftware.org/isdl.php
;   4. Open this file in Inno Setup Compiler and click Build
;
; Output: installer/BeaconSetup.exe
;
; What the installer does:
;   - Installs Beacon app + Guard to Program Files
;   - Installs Ollama silently (if not already installed)
;   - Creates desktop shortcut
;   - Optionally adds Guard to Windows startup
;   - Launches Beacon after install

[Setup]
AppName=Beacon
AppVersion=1.0.0
AppPublisher=Corey Redwine
AppPublisherURL=https://github.com/credwine/beacon
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
SetupIconFile=..\frontend\assets\icon-192.svg

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: checked
Name: "startupguard"; Description: "Start Beacon Guard on Windows startup (silent background protection)"; GroupDescription: "Background Protection:"; Flags: checked
Name: "installollama"; Description: "Install Ollama (required for AI features, free)"; GroupDescription: "AI Engine:"; Flags: checked; Check: not IsOllamaInstalled

[Files]
; Bundle everything from PyInstaller output
Source: "..\dist\Beacon\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
; Bundle Ollama installer (user must download to installer/ folder first)
Source: "OllamaSetup.exe"; DestDir: "{tmp}"; Flags: ignoreversion deleteafterinstall; Tasks: installollama; Check: FileExists(ExpandConstant('{src}\installer\OllamaSetup.exe'))

[Icons]
; Start menu
Name: "{group}\Beacon"; Filename: "{app}\Beacon.exe"; Comment: "AI-Powered Protection for Everyone"
Name: "{group}\Beacon Guard Monitor"; Filename: "{app}\Beacon.exe"; Parameters: "--monitor"; Comment: "Live security monitoring dashboard"
Name: "{group}\Uninstall Beacon"; Filename: "{uninstallexe}"

; Desktop
Name: "{autodesktop}\Beacon"; Filename: "{app}\Beacon.exe"; Tasks: desktopicon; Comment: "AI-Powered Protection for Everyone"

; Startup
Name: "{userstartup}\Beacon Guard"; Filename: "{app}\Beacon.exe"; Parameters: "--guard-only"; Tasks: startupguard

[Run]
; Install Ollama silently if selected
Filename: "{tmp}\OllamaSetup.exe"; Parameters: "/VERYSILENT /NORESTART"; StatusMsg: "Installing Ollama AI engine..."; Tasks: installollama; Flags: waituntilterminated
; Pull Gemma 4 model after Ollama install
Filename: "ollama"; Parameters: "pull gemma4:e4b"; StatusMsg: "Downloading Gemma 4 AI model (9.6 GB, one time)..."; Flags: waituntilterminated runhidden; Tasks: installollama
; Launch after install
Filename: "{app}\Beacon.exe"; Description: "Launch Beacon now"; Flags: postinstall nowait skipifsilent

[Code]
function IsOllamaInstalled: Boolean;
var
  ResultCode: Integer;
begin
  Result := Exec('ollama', '--version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0);
  if not Result then
  begin
    Result := FileExists(ExpandConstant('{localappdata}\Programs\Ollama\ollama.exe'));
  end;
end;

[Messages]
WelcomeLabel1=Welcome to Beacon
WelcomeLabel2=Beacon is a free, privacy-first AI tool that protects you from scams, explains contracts in plain English, and helps you know your rights.%n%nBeacon Guard runs silently in the background, monitoring your screen for phishing, scams, and dark patterns using AI -- and sends you a notification when something looks wrong.%n%nAll AI runs 100%% locally on your device. No data ever leaves your computer.
FinishedLabel=Beacon has been installed.%n%nDouble-click the Beacon icon on your desktop to start.%n%nBeacon Guard is set to start automatically and will protect you silently in the background.
