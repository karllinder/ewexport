# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for EWExport
# Optimized to reduce antivirus false positives

import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
    ],
    hiddenimports=[
        'tkinter',
        'striprtf',
        'packaging',
        'packaging.version',
        'packaging.specifiers',
        'packaging.requirements'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy', 
        'PIL',
        'scipy',
        'pandas',
        'pytest',
        'jinja2',
        'flask',
        'django',
        'cryptography',
        'bcrypt',
        'nacl',
        'pycparser',
        'cffi',
        'brotli',
        'lxml',
        'html5lib',
        'beautifulsoup4',
        'soupsieve',
        'pytz',
        'dateutil',
        'babel'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ewexport',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX compression
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.py',
    uac_admin=False,  # Don't request admin rights
    uac_uiaccess=False,
)