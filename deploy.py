#!/usr/bin/env python3
"""
🚀 نشر أوتوماتيكي لمنصة المسابقات الرياضية
Auto-deployment script for Math Competition Platform
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

def run_command(command, description=""):
    """تشغيل أمر مع عرض النتيجة"""
    print(f"🔄 {description}")
    print(f"📝 Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - نجح!")
            if result.stdout:
                print(f"📤 Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - فشل!")
            if result.stderr:
                print(f"🚨 Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ خطأ في تشغيل الأمر: {e}")
        return False

def setup_django():
    """إعداد Django"""
    print("\n🔧 إعداد Django...")
    
    commands = [
        ("python manage.py migrate", "تطبيق قاعدة البيانات"),
        ("python manage.py collectstatic --noinput", "جمع الملفات الثابتة"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def create_deployment_files():
    """إنشاء ملفات النشر"""
    print("\n📁 إنشاء ملفات النشر...")
    
    # ملف Procfile لـ Heroku
    procfile_content = "web: gunicorn alhassan.wsgi --log-file -"
    with open("Procfile", "w") as f:
        f.write(procfile_content)
    print("✅ تم إنشاء Procfile")
    
    # ملف runtime.txt
    runtime_content = "python-3.11.10"
    with open("runtime.txt", "w") as f:
        f.write(runtime_content)
    print("✅ تم إنشاء runtime.txt")
    
    # ملف app.json لـ Heroku
    app_json = {
        "name": "Math Competition Platform",
        "description": "منصة المسابقات الرياضية للتلاميذ",
        "keywords": ["django", "education", "math", "competition"],
        "website": "https://github.com/your-repo",
        "repository": "https://github.com/your-repo",
        "env": {
            "DJANGO_SECRET_KEY": {
                "description": "Django secret key",
                "generator": "secret"
            },
            "DEBUG": {
                "description": "Debug mode",
                "value": "False"
            }
        },
        "formation": {
            "web": {
                "quantity": 1,
                "size": "free"
            }
        },
        "addons": ["heroku-postgresql:mini"],
        "buildpacks": [
            {
                "url": "heroku/python"
            }
        ]
    }
    
    with open("app.json", "w", encoding='utf-8') as f:
        json.dump(app_json, f, indent=2, ensure_ascii=False)
    print("✅ تم إنشاء app.json")

def generate_deployment_urls():
    """إنشاء روابط النشر"""
    print("\n🌐 روابط النشر السريع:")
    
    # رابط Heroku Deploy
    heroku_url = "https://heroku.com/deploy?template=https://github.com/your-username/math-competition-platform"
    print(f"🟣 Heroku: {heroku_url}")
    
    # رابط Railway
    railway_url = "https://railway.app/new/template"
    print(f"🚂 Railway: {railway_url}")
    
    # رابط Render
    render_url = "https://render.com/deploy"
    print(f"🎨 Render: {render_url}")
    
    return {
        "heroku": heroku_url,
        "railway": railway_url,
        "render": render_url
    }

def start_local_server():
    """تشغيل الخادم المحلي"""
    print("\n🚀 تشغيل الخادم المحلي...")
    print("📍 الرابط المحلي: http://localhost:8000")
    print("👥 رابط التلاميذ: http://localhost:8000/student/login/")
    print("🔑 رمز الدخول للتلاميذ: ben25")
    print("\n⏹️  اضغط Ctrl+C لإيقاف الخادم")
    
    try:
        subprocess.run(["python", "manage.py", "runserver", "0.0.0.0:8000"])
    except KeyboardInterrupt:
        print("\n✅ تم إيقاف الخادم")

def main():
    """الدالة الرئيسية"""
    print("🎯 منصة المسابقات الرياضية - النشر الأوتوماتيكي")
    print("=" * 50)
    
    # التحقق من وجود Django
    try:
        import django
        print(f"✅ Django {django.get_version()} متوفر")
    except ImportError:
        print("❌ Django غير مثبت!")
        print("📦 تثبيت Django...")
        if not run_command("pip install Django==5.2.1", "تثبيت Django"):
            sys.exit(1)
    
    # إعداد Django
    if not setup_django():
        print("❌ فشل في إعداد Django")
        sys.exit(1)
    
    # إنشاء ملفات النشر
    create_deployment_files()
    
    # عرض روابط النشر
    urls = generate_deployment_urls()
    
    print("\n" + "=" * 50)
    print("🎉 تم الإعداد بنجاح!")
    print("=" * 50)
    
    print("\n📋 الخطوات التالية:")
    print("1️⃣ ارفع الملفات على GitHub")
    print("2️⃣ استخدم أحد روابط النشر أعلاه")
    print("3️⃣ أو شغل الخادم محلياً")
    
    # خيار تشغيل محلي
    choice = input("\n❓ هل تريد تشغيل الخادم محلياً الآن؟ (y/n): ").lower()
    if choice in ['y', 'yes', 'نعم']:
        start_local_server()
    else:
        print("\n✅ انتهى الإعداد. يمكنك الآن نشر التطبيق!")

if __name__ == "__main__":
    main()
