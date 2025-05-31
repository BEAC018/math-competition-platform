#!/usr/bin/env python3
"""
🚀 نشر أوتوماتيكي على Replit
Automatic Replit Deployment
"""

import os
import subprocess
import time
import webbrowser

def setup_replit_deployment():
    """إعداد النشر على Replit"""
    print("🚀 إعداد النشر على Replit...")
    
    # إنشاء ملف .replit محسن
    replit_config = '''run = "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"
language = "python3"

[nix]
channel = "stable-22_11"

[deployment]
run = ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
deploymentTarget = "cloudrun"

[env]
PYTHONPATH = "${REPL_HOME}:${PYTHONPATH}"
DJANGO_SETTINGS_MODULE = "alhassan.settings"

[interpreter]
command = ["python3", "-u"]

[gitHubImport]
requiredFiles = [".replit", "replit.nix", "requirements.txt"]

[languages]

[languages.python3]
pattern = "**/*.py"

[languages.python3.languageServer]
start = "pylsp"

[debugger]
support = true

[debugger.interactive]
transport = "localhost:5678"
startCommand = ["python", "-m", "debugpy", "--listen", "5678", "--wait-for-client", "-m", "flask", "run", "--no-debugger", "--no-reload", "--host", "0.0.0.0", "--port", "3000"]

[debugger.interactive.integratedAdapter]
dapTcpAddress = "localhost:5678"

[debugger.interactive.initializeMessage]
command = "initialize"
type = "request"

[debugger.interactive.initializeMessage.arguments]
adapterID = "debugpy"
clientID = "replit"
clientName = "replit.com"
columnsStartAt1 = true
linesStartAt1 = true
locale = "en-us"
pathFormat = "path"
supportsInvalidatedEvent = true
supportsProgressReporting = true
supportsRunInTerminalRequest = true
supportsVariablePaging = true
supportsVariableType = true

[debugger.interactive.launchMessage]
command = "attach"
type = "request"

[debugger.interactive.launchMessage.arguments]
logging = {}'''

    with open('.replit', 'w', encoding='utf-8') as f:
        f.write(replit_config)
    
    print("✅ تم إنشاء ملف .replit محسن")
    
    # إنشاء ملف replit.nix
    nix_config = '''{ pkgs }: {
  deps = [
    pkgs.python311Full
    pkgs.replitPackages.prybar-python311
    pkgs.replitPackages.stderred
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      # Needed for pandas / numpy
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      # Needed for pygame
      pkgs.glib
      # Needed for matplotlib
      pkgs.xorg.libX11
    ];
    PYTHONHOME = "${pkgs.python311Full}";
    PYTHONBIN = "${pkgs.python311Full}/bin/python3.11";
    LANG = "en_US.UTF-8";
    STDERREDBIN = "${pkgs.replitPackages.stderred}/bin/stderred";
    PRYBAR_PYTHON_BIN = "${pkgs.replitPackages.prybar-python311}/bin/prybar-python311";
  };
}'''

    with open('replit.nix', 'w', encoding='utf-8') as f:
        f.write(nix_config)
    
    print("✅ تم إنشاء ملف replit.nix")

def create_startup_script():
    """إنشاء سكريبت بدء التشغيل"""
    startup_script = '''#!/bin/bash
echo "🚀 بدء تشغيل منصة المسابقات الرياضية..."

# تثبيت المتطلبات
echo "📦 تثبيت المتطلبات..."
pip install -r requirements.txt

# إعداد قاعدة البيانات
echo "🗄️ إعداد قاعدة البيانات..."
python manage.py migrate

# جمع الملفات الثابتة
echo "📁 جمع الملفات الثابتة..."
python manage.py collectstatic --noinput

# تشغيل الخادم
echo "🌐 تشغيل الخادم..."
echo "📍 رابط المنصة: https://$REPL_SLUG.$REPL_OWNER.repl.co"
echo "👥 رابط التلاميذ: https://$REPL_SLUG.$REPL_OWNER.repl.co/student/login/"
echo "🔑 رمز الدخول: ben25"

python manage.py runserver 0.0.0.0:8000'''

    with open('start.sh', 'w', encoding='utf-8') as f:
        f.write(startup_script)
    
    # جعل الملف قابل للتنفيذ
    os.chmod('start.sh', 0o755)
    
    print("✅ تم إنشاء سكريبت البدء")

def run_deployment():
    """تشغيل النشر"""
    print("\n🔄 تشغيل النشر...")
    
    try:
        # تشغيل الإعداد
        subprocess.run(['python', 'manage.py', 'migrate'], check=True)
        print("✅ تم إعداد قاعدة البيانات")
        
        subprocess.run(['python', 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("✅ تم جمع الملفات الثابتة")
        
        print("\n🎉 تم الإعداد بنجاح!")
        print("🌐 يمكنك الآن الضغط على زر 'Run' في Replit")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ خطأ في الإعداد: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🎯 نشر منصة المسابقات الرياضية على Replit")
    print("=" * 50)
    
    # إعداد ملفات Replit
    setup_replit_deployment()
    
    # إنشاء سكريبت البدء
    create_startup_script()
    
    # تشغيل النشر
    if run_deployment():
        print("\n" + "=" * 50)
        print("🎉 تم النشر بنجاح!")
        print("=" * 50)
        
        print("\n📋 التعليمات:")
        print("1️⃣ اضغط زر 'Run' الأخضر في Replit")
        print("2️⃣ انتظر حتى يظهر الرابط")
        print("3️⃣ شارك الرابط مع التلاميذ")
        
        print("\n🔗 روابط مفيدة:")
        print("👥 للتلاميذ: [رابطك]/student/login/")
        print("🔑 رمز الدخول: ben25")
        print("👨‍🏫 للأساتذة: [رابطك]/accounts/login/")
        
    else:
        print("❌ فشل في النشر")

if __name__ == "__main__":
    main()
