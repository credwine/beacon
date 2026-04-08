# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['beacon_app.py'],
    pathex=[],
    binaries=[],
    datas=[('frontend', 'frontend'), ('backend/prompts', 'backend/prompts'), ('training/data', 'training/data'), ('guard', 'guard')],
    hiddenimports=['uvicorn.logging', 'uvicorn.loops', 'uvicorn.loops.auto', 'uvicorn.protocols', 'uvicorn.protocols.http', 'uvicorn.protocols.http.auto', 'uvicorn.protocols.websockets', 'uvicorn.protocols.websockets.auto', 'uvicorn.lifespan', 'uvicorn.lifespan.on', 'backend', 'backend.main', 'backend.routers', 'backend.routers.scanner', 'backend.routers.contracts', 'backend.routers.rights', 'backend.routers.streaming', 'backend.routers.alerts', 'backend.services', 'backend.services.scam_analyzer', 'backend.services.contract_analyzer', 'backend.services.rights_navigator', 'backend.services.prescreener', 'backend.services.alert_service', 'backend.ollama_client', 'backend.config', 'guard.beacon_guard', 'win10toast', 'PIL', 'psutil', 'plyer.platforms.win.notification'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Beacon',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Beacon',
)
