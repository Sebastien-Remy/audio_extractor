# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[
        ("/opt/homebrew/bin/ffmpeg", "."),
        ("/opt/homebrew/bin/ffprobe", "."),
    ],
    datas=[],
    hiddenimports=[],
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
    name="Audio Extractor",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Audio Extractor",
)

app = BUNDLE(
    coll,
    name="Audio Extractor.app",
    icon="img/audioextractor.icns",
    bundle_identifier="fr.gorilladev.audioextractor",
    info_plist={
        "CFBundleName": "Audio Extractor",
        "CFBundleDisplayName": "Audio Extractor",
        "CFBundleShortVersionString": "0.1",
        "CFBundleVersion": "1",
        "NSHighResolutionCapable": True,
    },
)
