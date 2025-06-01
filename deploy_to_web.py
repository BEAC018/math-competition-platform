#!/usr/bin/env python3
"""
🌐 نشر تلقائي لمنصة المسابقات الرياضية على الويب
سيقوم هذا السكريبت بنشر المشروع تلقائياً على أفضل منصة متاحة
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    """طباعة شعار البرنامج"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🌐 نشر منصة المسابقات الرياضية على الويب           ║
    ║                                                              ║
    ║              🚀 نشر تلقائي وسريع وآمن                      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """التحقق من المتطلبات"""
    print("🔍 التحقق من المتطلبات...")
    
    # التحقق من Git
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        print("✅ Git متوفر")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git غير مثبت")
        return False
    
    # التحقق من مجلد Git
    if not Path('.git').exists():
        print("❌ هذا المجلد ليس مشروع Git")
        return False
    
    print("✅ جميع المتطلبات متوفرة")
    return True

def prepare_for_deployment():
    """تحضير المشروع للنشر"""
    print("\n⚙️  تحضير المشروع للنشر...")
    
    # التحقق من الملفات المطلوبة
    required_files = ['requirements.txt', 'manage.py', 'alhassan/settings.py']
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ الملف المطلوب غير موجود: {file}")
            return False
    
    print("✅ جميع الملفات المطلوبة موجودة")
    
    # حفظ التغييرات في Git
    try:
        # إضافة جميع الملفات
        subprocess.run(['git', 'add', '.'], check=True)
        
        # التحقق من وجود تغييرات
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            # إنشاء commit
            commit_msg = "deploy: تحضير للنشر التلقائي على الويب"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            
            # رفع إلى GitHub
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            print("✅ تم حفظ ورفع التغييرات")
        else:
            print("✅ لا توجد تغييرات جديدة")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ خطأ في Git: {e}")
        return False

def show_platform_options():
    """عرض خيارات المنصات"""
    print("\n" + "=" * 60)
    print("🎯 اختر منصة النشر:")
    print("=" * 60)
    print()
    print("1️⃣  Railway (موصى به)")
    print("   ✅ مجاني حتى 5$ شهرياً")
    print("   ✅ لا ينام أبداً (متاح 24/7)")
    print("   ✅ سريع جداً في النشر")
    print("   ✅ PostgreSQL مجاني")
    print("   ✅ مناسب للمشاريع التعليمية")
    print()
    print("2️⃣  Render (مجاني)")
    print("   ✅ مجاني تماماً (750 ساعة شهرياً)")
    print("   ✅ سهل جداً للمبتدئين")
    print("   ✅ PostgreSQL مجاني")
    print("   ⚠️  ينام بعد 15 دقيقة من عدم النشاط")
    print()
    print("3️⃣  اختيار تلقائي (Railway)")
    print("   🤖 سأختار أفضل منصة لك")
    print()

def deploy_to_railway():
    """النشر على Railway"""
    print("\n🚀 بدء النشر على Railway...")
    
    # فتح صفحة Railway
    github_repo = "BEAC1/math-competition-platform"
    railway_url = f"https://railway.app/new/template?template=https://github.com/{github_repo}"
    
    print(f"🌐 فتح Railway: {railway_url}")
    webbrowser.open(railway_url)
    
    # عرض التعليمات
    print("\n📋 اتبع هذه الخطوات:")
    print("1️⃣ سجل دخول بـ GitHub")
    print("2️⃣ انقر 'Deploy Now'")
    print("3️⃣ أضف PostgreSQL: New Service > Database > PostgreSQL")
    print("4️⃣ أضف متغيرات البيئة:")
    print("   DJANGO_SECRET_KEY = django-insecure-railway-production-key-2025")
    print("   DEBUG = False")
    print("   ALLOWED_HOSTS = *.railway.app,*.up.railway.app")
    print("5️⃣ احصل على الرابط من Settings > Generate Domain")
    
    return railway_url

def deploy_to_render():
    """النشر على Render"""
    print("\n🌟 بدء النشر على Render...")
    
    # فتح صفحة Render
    render_url = "https://render.com"
    print(f"🌐 فتح Render: {render_url}")
    webbrowser.open(render_url)
    
    # عرض التعليمات
    print("\n📋 اتبع هذه الخطوات:")
    print("1️⃣ سجل دخول بـ GitHub")
    print("2️⃣ انقر 'New +' > 'Web Service'")
    print("3️⃣ اربط repository: math-competition-platform")
    print("4️⃣ إعدادات:")
    print("   Build Command: pip install -r requirements.txt")
    print("   Start Command: gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT")
    print("5️⃣ أضف متغيرات البيئة:")
    print("   DJANGO_SECRET_KEY = django-insecure-render-production-key-2025")
    print("   DEBUG = False")
    print("   ALLOWED_HOSTS = *.onrender.com")
    print("6️⃣ أنشئ PostgreSQL منفصل واربط DATABASE_URL")
    
    return render_url

def get_deployment_result():
    """الحصول على نتيجة النشر"""
    print("\n" + "=" * 60)
    print("⏳ انتظار اكتمال النشر...")
    print("=" * 60)
    
    input("\n⏸️  اضغط Enter بعد اكتمال النشر...")
    
    print("\n🔗 أدخل رابط مشروعك:")
    project_url = input("الرابط: ").strip()
    
    if project_url:
        # التحقق من صحة الرابط
        if not project_url.startswith('http'):
            project_url = 'https://' + project_url
        
        print(f"\n🎊 مبروك! مشروعك متاح على: {project_url}")
        print(f"🎓 للطلاب: {project_url}/student/login/ (الرمز: ben25)")
        print(f"👨‍🏫 للمعلمين: {project_url}/accounts/login/")
        
        # حفظ الرابط
        with open('LIVE_PROJECT_URL.txt', 'w', encoding='utf-8') as f:
            f.write(f"🌐 رابط المشروع المباشر: {project_url}\n")
            f.write(f"🎓 رابط الطلاب: {project_url}/student/login/\n")
            f.write(f"👨‍🏫 رابط المعلمين: {project_url}/accounts/login/\n")
            f.write(f"🔑 رمز دخول الطلاب: ben25\n")
            f.write(f"📅 تاريخ النشر: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print("💾 تم حفظ الرابط في LIVE_PROJECT_URL.txt")
        
        # اختبار الرابط
        print(f"\n🧪 اختبار الرابط...")
        webbrowser.open(project_url)
        
        return project_url
    
    return None

def show_success_message(project_url):
    """عرض رسالة النجاح"""
    success_banner = f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                    🎉 تم النشر بنجاح! 🎉                   ║
    ║                                                              ║
    ║  مشروعك متاح الآن للعالم على الإنترنت                     ║
    ║                                                              ║
    ║  🌐 الرابط: {project_url:<45} ║
    ║                                                              ║
    ║  🎓 للطلاب: /student/login/ (الرمز: ben25)                 ║
    ║  👨‍🏫 للمعلمين: /accounts/login/                            ║
    ║                                                              ║
    ║  📤 شارك الرابط مع الطلاب والمعلمين!                     ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(success_banner)

def main():
    """الدالة الرئيسية"""
    print_banner()
    
    # التحقق من المتطلبات
    if not check_requirements():
        print("\n❌ لا يمكن المتابعة بدون المتطلبات")
        return
    
    # تحضير المشروع
    if not prepare_for_deployment():
        print("\n❌ فشل في تحضير المشروع")
        return
    
    # عرض خيارات المنصات
    show_platform_options()
    
    # اختيار المنصة
    while True:
        choice = input("اختر رقم المنصة (1-3): ").strip()
        
        if choice == '1':
            deploy_url = deploy_to_railway()
            break
        elif choice == '2':
            deploy_url = deploy_to_render()
            break
        elif choice == '3':
            print("🤖 اختيار تلقائي: Railway (الأفضل للمشاريع التعليمية)")
            deploy_url = deploy_to_railway()
            break
        else:
            print("❌ اختيار غير صحيح، جرب مرة أخرى")
    
    # الحصول على نتيجة النشر
    project_url = get_deployment_result()
    
    if project_url:
        show_success_message(project_url)
    else:
        print("\n⚠️  لم يتم إدخال رابط المشروع")
        print("💡 يمكنك إضافة الرابط لاحقاً في ملف LIVE_PROJECT_URL.txt")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  تم إيقاف العملية بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        print("💡 تأكد من أن Git مثبت وأنك في مجلد المشروع الصحيح")
    
    input("\n⏸️  اضغط Enter للخروج...")
