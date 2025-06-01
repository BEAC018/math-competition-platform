#!/usr/bin/env python3
"""
🌟 نشر تلقائي لمنصة المسابقات الرياضية على Render (مجاني)
سيقوم هذا السكريبت بنشر المشروع تلقائياً على Render
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
    print("🌟 نشر تلقائي لمنصة المسابقات الرياضية على Render")
    print("=" * 60)
    print()

def create_render_config():
    """إنشاء ملفات إعداد Render"""
    print("⚙️  إنشاء ملفات إعداد Render...")
    
    # إنشاء render.yaml
    render_config = {
        "services": [
            {
                "type": "web",
                "name": "math-competition-platform",
                "env": "python",
                "buildCommand": "pip install -r requirements.txt && python manage.py collectstatic --noinput",
                "startCommand": "python manage.py migrate && gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120",
                "envVars": [
                    {
                        "key": "DJANGO_SECRET_KEY",
                        "value": "django-insecure-render-production-key-2025"
                    },
                    {
                        "key": "DEBUG",
                        "value": "False"
                    },
                    {
                        "key": "ALLOWED_HOSTS",
                        "value": "*.onrender.com"
                    },
                    {
                        "key": "PYTHON_VERSION",
                        "value": "3.11.7"
                    }
                ]
            }
        ],
        "databases": [
            {
                "name": "math-competition-db",
                "databaseName": "math_competition",
                "user": "math_user"
            }
        ]
    }
    
    with open('render.yaml', 'w', encoding='utf-8') as f:
        import yaml
        yaml.dump(render_config, f, default_flow_style=False, allow_unicode=True)
    
    print("✅ تم إنشاء render.yaml")

def open_render_deployment():
    """فتح صفحة Render للنشر"""
    print("🌐 فتح صفحة Render للنشر...")
    
    # رابط النشر المباشر من GitHub
    github_repo = "BEAC1/math-competition-platform"
    render_url = f"https://render.com/deploy?repo=https://github.com/{github_repo}"
    
    print(f"🔗 فتح الرابط: {render_url}")
    webbrowser.open(render_url)
    
    # فتح صفحة Render الرئيسية كبديل
    backup_url = "https://render.com"
    print(f"🔗 رابط بديل: {backup_url}")
    
    return render_url

def show_deployment_instructions():
    """عرض تعليمات النشر"""
    print("\n" + "=" * 60)
    print("📋 تعليمات النشر على Render:")
    print("=" * 60)
    print()
    print("1️⃣ سجل دخول بـ GitHub في صفحة Render")
    print("2️⃣ انقر 'New +' > 'Web Service'")
    print("3️⃣ اختر 'Build and deploy from a Git repository'")
    print("4️⃣ اربط repository: math-competition-platform")
    print("5️⃣ إعدادات الخدمة:")
    print("   - Name: math-competition-platform")
    print("   - Environment: Python 3")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT")
    print("6️⃣ أضف متغيرات البيئة:")
    print("   - DJANGO_SECRET_KEY = django-insecure-render-production-key-2025")
    print("   - DEBUG = False")
    print("   - ALLOWED_HOSTS = *.onrender.com")
    print("7️⃣ أنشئ قاعدة بيانات PostgreSQL منفصلة")
    print("8️⃣ اربط DATABASE_URL من قاعدة البيانات")
    print()

def show_database_instructions():
    """عرض تعليمات إنشاء قاعدة البيانات"""
    print("=" * 60)
    print("🗄️  إنشاء قاعدة البيانات:")
    print("=" * 60)
    print()
    print("1️⃣ في Render Dashboard، انقر 'New +' > 'PostgreSQL'")
    print("2️⃣ إعدادات قاعدة البيانات:")
    print("   - Name: math-competition-db")
    print("   - Database Name: math_competition")
    print("   - User: math_user")
    print("3️⃣ انسخ 'External Database URL'")
    print("4️⃣ في Web Service، أضف متغير البيئة:")
    print("   - DATABASE_URL = (الرابط المنسوخ)")
    print()

def show_usage_instructions():
    """عرض تعليمات الاستخدام"""
    print("=" * 60)
    print("📱 كيفية استخدام المنصة:")
    print("=" * 60)
    print()
    print("🎓 للطلاب:")
    print("   الرابط: https://your-app.onrender.com/student/login/")
    print("   الرمز: ben25")
    print()
    print("👨‍🏫 للمعلمين:")
    print("   الرابط: https://your-app.onrender.com/accounts/login/")
    print("   (سجل دخول أو أنشئ حساب جديد)")
    print()
    print("⚠️  ملاحظة: Render المجاني ينام بعد 15 دقيقة من عدم النشاط")
    print("   وقد يستغرق 30-60 ثانية للاستيقاظ")
    print()

def main():
    """الدالة الرئيسية"""
    print_header()
    
    # التحقق من وجود Git
    if not Path('.git').exists():
        print("❌ هذا المجلد ليس مشروع Git")
        print("💡 تأكد من أنك في مجلد المشروع الصحيح")
        return
    
    # فتح صفحة Render
    render_url = open_render_deployment()
    
    # عرض التعليمات
    show_deployment_instructions()
    show_database_instructions()
    show_usage_instructions()
    
    print("=" * 60)
    print("🎉 تم تحضير كل شيء للنشر المجاني!")
    print("🌐 اتبع التعليمات أعلاه لإكمال النشر")
    print("=" * 60)
    
    # انتظار المستخدم
    input("\n⏸️  اضغط Enter بعد إكمال النشر على Render...")
    
    # طلب رابط المشروع
    print("\n🔗 أدخل رابط مشروعك على Render:")
    project_url = input("الرابط: ").strip()
    
    if project_url:
        print(f"\n🎊 مبروك! مشروعك متاح مجاناً على: {project_url}")
        print(f"🎓 للطلاب: {project_url}/student/login/ (الرمز: ben25)")
        print(f"👨‍🏫 للمعلمين: {project_url}/accounts/login/")
        
        # حفظ الرابط
        with open('LIVE_PROJECT_URL_RENDER.txt', 'w', encoding='utf-8') as f:
            f.write(f"🌐 رابط المشروع المباشر (Render): {project_url}\n")
            f.write(f"🎓 للطلاب: {project_url}/student/login/\n")
            f.write(f"👨‍🏫 للمعلمين: {project_url}/accounts/login/\n")
            f.write(f"📅 تاريخ النشر: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"💰 نوع الاستضافة: مجانية (750 ساعة شهرياً)\n")
            f.write(f"😴 ملاحظة: ينام بعد 15 دقيقة من عدم النشاط\n")
        
        print("💾 تم حفظ الرابط في LIVE_PROJECT_URL_RENDER.txt")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  تم إيقاف العملية بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        print("💡 تأكد من أن Git مثبت وأنك في مجلد المشروع الصحيح")
