#!/usr/bin/env python3
"""
🚀 نشر تلقائي لمنصة المسابقات الرياضية على Railway
سيقوم هذا السكريبت بنشر المشروع تلقائياً على Railway
"""

import os
import sys
import time
import json
import subprocess
import webbrowser
from pathlib import Path

def print_header():
    """طباعة رأس البرنامج"""
    print("=" * 60)
    print("🚀 نشر تلقائي لمنصة المسابقات الرياضية على Railway")
    print("=" * 60)
    print()

def check_git_status():
    """التحقق من حالة Git"""
    print("🔍 التحقق من حالة Git...")
    try:
        git_cmd = r"C:\Program Files\Git\bin\git.exe"
        result = subprocess.run([git_cmd, 'status', '--porcelain'],
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("⚠️  يوجد تغييرات غير محفوظة في Git")
            print("📤 سيتم حفظ التغييرات ورفعها...")
            return False
        else:
            print("✅ Git محدث ونظيف")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ خطأ في التحقق من Git")
        return False

def commit_and_push():
    """حفظ ورفع التغييرات إلى GitHub"""
    print("📤 حفظ ورفع التغييرات...")
    try:
        git_cmd = r"C:\Program Files\Git\bin\git.exe"
        # إضافة جميع الملفات
        subprocess.run([git_cmd, 'add', '.'], check=True)

        # إنشاء commit
        commit_msg = "deploy: تحضير للنشر التلقائي على Railway"
        subprocess.run([git_cmd, 'commit', '-m', commit_msg], check=True)

        # رفع إلى GitHub
        subprocess.run([git_cmd, 'push', 'origin', 'main'], check=True)

        print("✅ تم رفع التغييرات إلى GitHub بنجاح")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ خطأ في رفع التغييرات: {e}")
        return False

def create_railway_config():
    """إنشاء ملفات إعداد Railway"""
    print("⚙️  إنشاء ملفات إعداد Railway...")

    # إنشاء railway.json محسن
    railway_config = {
        "$schema": "https://railway.app/railway.schema.json",
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120",
            "healthcheckPath": "/",
            "healthcheckTimeout": 100,
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }

    with open('railway.json', 'w', encoding='utf-8') as f:
        json.dump(railway_config, f, indent=2, ensure_ascii=False)

    print("✅ تم إنشاء railway.json")

def open_railway_deployment():
    """فتح صفحة Railway للنشر"""
    print("🌐 فتح صفحة Railway للنشر...")

    # رابط النشر المباشر من GitHub
    github_repo = "BEAC1/math-competition-platform"
    railway_url = f"https://railway.app/new/template?template=https://github.com/{github_repo}"

    print(f"🔗 فتح الرابط: {railway_url}")
    webbrowser.open(railway_url)

    return railway_url

def show_deployment_instructions():
    """عرض تعليمات النشر"""
    print("\n" + "=" * 60)
    print("📋 تعليمات النشر على Railway:")
    print("=" * 60)
    print()
    print("1️⃣ سجل دخول بـ GitHub في الصفحة التي فتحت")
    print("2️⃣ انقر 'Deploy Now' لبدء النشر")
    print("3️⃣ انتظر 5-10 دقائق لاكتمال النشر")
    print("4️⃣ أضف قاعدة بيانات PostgreSQL:")
    print("   - انقر 'New Service' > 'Database' > 'PostgreSQL'")
    print("5️⃣ أضف متغيرات البيئة:")
    print("   - DJANGO_SECRET_KEY = django-insecure-railway-production-key-2025")
    print("   - DEBUG = False")
    print("   - ALLOWED_HOSTS = *.railway.app,*.up.railway.app")
    print("6️⃣ احصل على الرابط من Settings > Generate Domain")
    print()

def show_usage_instructions():
    """عرض تعليمات الاستخدام"""
    print("=" * 60)
    print("📱 كيفية استخدام المنصة:")
    print("=" * 60)
    print()
    print("🎓 للطلاب:")
    print("   الرابط: https://your-app.railway.app/student/login/")
    print("   الرمز: ben25")
    print()
    print("👨‍🏫 للمعلمين:")
    print("   الرابط: https://your-app.railway.app/accounts/login/")
    print("   (سجل دخول أو أنشئ حساب جديد)")
    print()

def main():
    """الدالة الرئيسية"""
    print_header()

    # التحقق من وجود Git
    if not Path('.git').exists():
        print("❌ هذا المجلد ليس مشروع Git")
        print("💡 تأكد من أنك في مجلد المشروع الصحيح")
        return

    # التحقق من حالة Git
    git_clean = check_git_status()

    # حفظ ورفع التغييرات إذا لزم الأمر
    if not git_clean:
        if not commit_and_push():
            print("❌ فشل في رفع التغييرات")
            return

    # إنشاء ملفات إعداد Railway
    create_railway_config()

    # حفظ ملفات الإعداد الجديدة
    print("📤 حفظ ملفات الإعداد...")
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'config: تحديث إعدادات Railway للنشر'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ تم حفظ ملفات الإعداد")
    except subprocess.CalledProcessError:
        print("⚠️  تعذر حفظ ملفات الإعداد (قد تكون محفوظة مسبقاً)")

    # فتح صفحة Railway
    railway_url = open_railway_deployment()

    # عرض التعليمات
    show_deployment_instructions()
    show_usage_instructions()

    print("=" * 60)
    print("🎉 تم تحضير كل شيء للنشر!")
    print("🌐 اتبع التعليمات أعلاه لإكمال النشر")
    print("=" * 60)

    # انتظار المستخدم
    input("\n⏸️  اضغط Enter بعد إكمال النشر على Railway...")

    # طلب رابط المشروع
    print("\n🔗 أدخل رابط مشروعك على Railway:")
    project_url = input("الرابط: ").strip()

    if project_url:
        print(f"\n🎊 مبروك! مشروعك متاح على: {project_url}")
        print(f"🎓 للطلاب: {project_url}/student/login/ (الرمز: ben25)")
        print(f"👨‍🏫 للمعلمين: {project_url}/accounts/login/")

        # حفظ الرابط
        with open('LIVE_PROJECT_URL.txt', 'w', encoding='utf-8') as f:
            f.write(f"🌐 رابط المشروع المباشر: {project_url}\n")
            f.write(f"🎓 للطلاب: {project_url}/student/login/\n")
            f.write(f"👨‍🏫 للمعلمين: {project_url}/accounts/login/\n")
            f.write(f"📅 تاريخ النشر: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        print("💾 تم حفظ الرابط في LIVE_PROJECT_URL.txt")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  تم إيقاف العملية بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        print("💡 تأكد من أن Git مثبت وأنك في مجلد المشروع الصحيح")
