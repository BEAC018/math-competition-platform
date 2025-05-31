#!/usr/bin/env python3
"""
سكريبت بناء الملف التنفيذي لمنصة المسابقات الرياضية
Build script for Math Competition Platform executable
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import zipfile
from datetime import datetime

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully")
    except subprocess.CalledProcessError:
        print("Failed to install PyInstaller")
        return False
    return True

def create_spec_file():
    """إنشاء ملف .spec لـ PyInstaller"""

    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

BASE_DIR = Path(SPECPATH)

block_cipher = None

# جمع جميع ملفات Django
django_files = []

# إضافة ملفات التطبيق
app_dirs = ['alhassan', 'competitions', 'accounts', 'dashboard']
for app_dir in app_dirs:
    app_path = BASE_DIR / app_dir
    if app_path.exists():
        for root, dirs, files in os.walk(app_path):
            for file in files:
                if file.endswith(('.py', '.html', '.css', '.js', '.json')):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, BASE_DIR)
                    django_files.append((file_path, os.path.dirname(rel_path)))

# إضافة ملفات القوالب
templates_path = BASE_DIR / 'templates'
if templates_path.exists():
    for root, dirs, files in os.walk(templates_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, BASE_DIR)
            django_files.append((file_path, os.path.dirname(rel_path)))

# إضافة الملفات الثابتة
static_path = BASE_DIR / 'static'
if static_path.exists():
    for root, dirs, files in os.walk(static_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, BASE_DIR)
            django_files.append((file_path, os.path.dirname(rel_path)))

# إضافة قاعدة البيانات
db_path = BASE_DIR / 'db.sqlite3'
if db_path.exists():
    django_files.append((str(db_path), '.'))

# إضافة manage.py
manage_path = BASE_DIR / 'manage.py'
if manage_path.exists():
    django_files.append((str(manage_path), '.'))

a = Analysis(
    ['launcher.py'],
    pathex=[str(BASE_DIR)],
    binaries=[],
    datas=django_files,
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
        'competitions.models',
        'competitions.views',
        'competitions.urls',
        'accounts',
        'dashboard',
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
        'psycopg2',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    icon='static/favicon.ico' if (BASE_DIR / 'static' / 'favicon.ico').exists() else None,
)
'''

    with open('math_platform.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print("✅ تم إنشاء ملف .spec")

def build_executable():
    """بناء الملف التنفيذي"""
    print("🔨 بناء الملف التنفيذي...")

    try:
        # تشغيل PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            "math_platform.spec"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ تم بناء الملف التنفيذي بنجاح")
            return True
        else:
            print("❌ فشل في بناء الملف التنفيذي")
            print("خطأ:", result.stderr)
            return False

    except Exception as e:
        print(f"❌ خطأ في البناء: {e}")
        return False

def create_distribution_package():
    """إنشاء حزمة التوزيع"""
    print("📦 إنشاء حزمة التوزيع...")

    dist_dir = Path("dist")
    exe_path = dist_dir / "MathCompetitionPlatform.exe"

    if not exe_path.exists():
        print("❌ لم يتم العثور على الملف التنفيذي")
        return False

    # إنشاء مجلد التوزيع
    package_name = f"MathCompetitionPlatform_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    package_dir = Path(package_name)

    if package_dir.exists():
        shutil.rmtree(package_dir)

    package_dir.mkdir()

    # نسخ الملف التنفيذي
    shutil.copy2(exe_path, package_dir / "MathCompetitionPlatform.exe")

    # إنشاء ملف README
    readme_content = """# منصة المسابقات الرياضية - Math Competition Platform

## 🚀 تعليمات التشغيل:

### للمستخدمين العاديين:
1. انقر نقراً مزدوجاً على `MathCompetitionPlatform.exe`
2. اضغط "بدء الخادم" في النافذة التي تظهر
3. انتظر حتى يصبح الخادم جاهزاً
4. سيفتح المتصفح تلقائياً على صفحة دخول الطلاب
5. استخدم رمز الدخول: `ben25`

### الروابط المهمة:
- **دخول الطلاب:** http://localhost:8000/student/login/
- **رمز الدخول:** ben25
- **دخول المعلمين:** http://localhost:8000/accounts/login/

### الميزات:
✅ تطبيق مستقل - لا يحتاج Python
✅ قاعدة بيانات مدمجة
✅ واجهة سهلة الاستخدام
✅ يعمل بنقرة واحدة
✅ يفتح المتصفح تلقائياً

### المتطلبات:
- نظام Windows 10 أو أحدث
- 100 MB مساحة فارغة
- متصفح ويب (Chrome, Firefox, Edge)

### استكشاف الأخطاء:
- إذا لم يعمل التطبيق، تأكد من أن المنفذ 8000 غير مستخدم
- إذا لم يفتح المتصفح، افتحه يدوياً واذهب إلى localhost:8000
- للدعم الفني، راجع الوثائق المرفقة

### إيقاف التطبيق:
- اضغط "إيقاف الخادم" في النافذة
- أو أغلق النافذة مباشرة

---

## 🎯 Math Competition Platform

### Quick Start:
1. Double-click `MathCompetitionPlatform.exe`
2. Click "Start Server" in the window
3. Wait for server to be ready
4. Browser will open automatically
5. Use login code: `ben25`

### Features:
✅ Standalone application
✅ Built-in database
✅ Easy-to-use interface
✅ One-click operation
✅ Auto-opens browser

Enjoy using the Math Competition Platform! 🧮
"""

    with open(package_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)

    # إنشاء ملف مضغوط
    zip_filename = f"{package_name}.zip"

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arc_name = file_path.relative_to(package_dir)
                zipf.write(file_path, arc_name)

    print(f"✅ تم إنشاء حزمة التوزيع: {zip_filename}")

    # عرض معلومات الحزمة
    exe_size = exe_path.stat().st_size / (1024 * 1024)
    zip_size = Path(zip_filename).stat().st_size / (1024 * 1024)

    print(f"📊 حجم الملف التنفيذي: {exe_size:.1f} MB")
    print(f"📦 حجم الحزمة المضغوطة: {zip_size:.1f} MB")

    return True

def main():
    """الدالة الرئيسية"""
    print("Building Math Competition Platform as executable...")
    print("=" * 50)

    # التحقق من وجود الملفات المطلوبة
    required_files = ['launcher.py', 'manage.py', 'alhassan/settings.py']
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ الملف المطلوب غير موجود: {file_path}")
            return False

    # تثبيت PyInstaller
    if not install_pyinstaller():
        return False

    # إنشاء ملف .spec
    create_spec_file()

    # بناء الملف التنفيذي
    if not build_executable():
        return False

    # إنشاء حزمة التوزيع
    if not create_distribution_package():
        return False

    print("\n" + "=" * 50)
    print("🎉 تم بناء التطبيق بنجاح!")
    print("=" * 50)
    print("📁 ستجد الملف التنفيذي في مجلد dist/")
    print("📦 ستجد حزمة التوزيع كملف مضغوط")
    print("📋 اقرأ ملف README.txt للتعليمات")

    print("\n🎯 التطبيق جاهز للتوزيع والمشاركة!")

    return True

if __name__ == "__main__":
    success = main()
    if not success:
        input("اضغط Enter للخروج...")
    else:
        input("اضغط Enter للخروج...")
