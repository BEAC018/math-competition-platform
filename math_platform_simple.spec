# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

BASE_DIR = Path(SPECPATH)

a = Analysis(
    ['launcher.py'],
    pathex=[str(BASE_DIR)],
    binaries=[],
    datas=[
        ('alhassan', 'alhassan'),
        ('competitions', 'competitions'),
        ('templates', 'templates'),
        ('static', 'static'),
        ('db.sqlite3', '.'),
        ('manage.py', '.'),
    ],
    hiddenimports=[
        'django',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'alhassan',
        'alhassan.settings',
        'alhassan.urls',
        'alhassan.wsgi',
        'competitions',
        'tkinter',
        'tkinter.ttk',
        'webbrowser',
        'threading',
        'socket',
        'subprocess',
        'pandas',
        'openpyxl',
        'reportlab',
        'PIL',
        'whitenoise',
        'dj_database_url',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MathCompetitionPlatform',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
