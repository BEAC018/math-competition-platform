#!/usr/bin/env python3
"""
Simple build script for Math Competition Platform executable
"""

import sys
import shutil
import subprocess
from pathlib import Path
import zipfile
from datetime import datetime

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # Create simple spec content
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

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
'''
    
    # Write spec file
    with open('math_platform_simple.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("Created spec file")
    
    try:
        # Run PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            "math_platform_simple.spec"
        ]
        
        print("Running PyInstaller...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Build successful!")
            return True
        else:
            print("Build failed!")
            print("Error:", result.stderr)
            return False
            
    except Exception as e:
        print(f"Build error: {e}")
        return False

def create_package():
    """Create distribution package"""
    print("Creating distribution package...")
    
    dist_dir = Path("dist")
    exe_path = dist_dir / "MathCompetitionPlatform.exe"
    
    if not exe_path.exists():
        print("Executable not found!")
        return False
    
    # Create package directory
    package_name = f"MathCompetitionPlatform_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    package_dir = Path(package_name)
    
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # Copy executable
    shutil.copy2(exe_path, package_dir / "MathCompetitionPlatform.exe")
    
    # Create README
    readme_content = """Math Competition Platform - Executable Version

QUICK START:
1. Double-click MathCompetitionPlatform.exe
2. Click "Start Server" button
3. Wait for server to be ready
4. Browser will open automatically
5. Use login code: ben25

LINKS:
- Student Login: http://localhost:8000/student/login/
- Login Code: ben25
- Teacher Login: http://localhost:8000/accounts/login/

FEATURES:
- Standalone application (no Python required)
- Built-in database
- Easy-to-use interface
- One-click operation
- Auto-opens browser

REQUIREMENTS:
- Windows 10 or newer
- 100 MB free space
- Web browser (Chrome, Firefox, Edge)

TROUBLESHOOTING:
- If app doesn't start, check that port 8000 is not in use
- If browser doesn't open, manually go to localhost:8000
- To stop: click "Stop Server" or close window

Enjoy using the Math Competition Platform!
"""
    
    with open(package_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Create zip file
    zip_filename = f"{package_name}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arc_name = file_path.relative_to(package_dir)
                zipf.write(file_path, arc_name)
    
    print(f"Package created: {zip_filename}")
    
    # Show file sizes
    exe_size = exe_path.stat().st_size / (1024 * 1024)
    zip_size = Path(zip_filename).stat().st_size / (1024 * 1024)
    
    print(f"Executable size: {exe_size:.1f} MB")
    print(f"Package size: {zip_size:.1f} MB")
    
    return True

def main():
    """Main function"""
    print("Building Math Competition Platform executable...")
    print("=" * 50)
    
    # Check required files
    required_files = ['launcher.py', 'manage.py', 'alhassan/settings.py']
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"Required file not found: {file_path}")
            return False
    
    # Install PyInstaller
    print("Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully")
    except subprocess.CalledProcessError:
        print("Failed to install PyInstaller")
        return False
    
    # Build executable
    if not build_executable():
        return False
    
    # Create package
    if not create_package():
        return False
    
    print("\n" + "=" * 50)
    print("Build completed successfully!")
    print("=" * 50)
    print("Find the executable in dist/ folder")
    print("Find the distribution package as zip file")
    print("Read README.txt for instructions")
    
    print("\nThe application is ready for distribution!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        input("Press Enter to exit...")
    else:
        input("Press Enter to exit...")
