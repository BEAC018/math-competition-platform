#!/usr/bin/env python3
"""
🔧 إصلاح مشاكل النشر
سيقوم هذا السكريبت بتشخيص وإصلاح مشاكل النشر
"""

import webbrowser
import time

def print_header():
    """طباعة رأس البرنامج"""
    print("=" * 60)
    print("🔧 إصلاح مشاكل النشر - منصة المسابقات الرياضية")
    print("=" * 60)
    print()

def diagnose_problem():
    """تشخيص المشكلة"""
    print("🔍 تشخيص مشكلة 404...")
    print()
    print("❌ المشكلة: صفحة 404 في Railway")
    print()
    print("🔍 الأسباب المحتملة:")
    print("1️⃣ المشروع لم يكتمل بناؤه")
    print("2️⃣ متغيرات البيئة مفقودة")
    print("3️⃣ قاعدة البيانات غير مربوطة")
    print("4️⃣ أخطاء في إعدادات Django")
    print()

def show_railway_fix():
    """عرض حل Railway"""
    print("🚀 الحل الأول: إصلاح Railway")
    print("=" * 40)
    print()
    print("1️⃣ تحقق من Build Logs:")
    print("   - اذهب إلى Railway Dashboard")
    print("   - انقر على مشروعك")
    print("   - تحقق من Deployments > Build Logs")
    print()
    print("2️⃣ أضف متغيرات البيئة:")
    print("   في Variables tab:")
    print("   DJANGO_SECRET_KEY = django-insecure-railway-production-key-2025")
    print("   DEBUG = False")
    print("   ALLOWED_HOSTS = *.railway.app,*.up.railway.app")
    print()
    print("3️⃣ أضف PostgreSQL:")
    print("   - New Service > Database > PostgreSQL")
    print()
    print("4️⃣ أعد النشر:")
    print("   - Deployments > Redeploy")
    print()

def show_render_alternative():
    """عرض بديل Render"""
    print("🌟 الحل البديل: Render (مجاني)")
    print("=" * 40)
    print()
    print("1️⃣ سجل دخول في Render")
    print("2️⃣ New + > Web Service")
    print("3️⃣ اربط GitHub repository")
    print("4️⃣ إعدادات:")
    print("   Build: pip install -r requirements.txt")
    print("   Start: gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT")
    print("5️⃣ متغيرات البيئة:")
    print("   DJANGO_SECRET_KEY = django-insecure-render-key-2025")
    print("   DEBUG = False")
    print("   ALLOWED_HOSTS = *.onrender.com")
    print()

def open_solutions():
    """فتح صفحات الحلول"""
    print("🌐 فتح صفحات الحلول...")
    
    # فتح Railway الجديد
    print("🚀 فتح Railway للنشر الجديد...")
    webbrowser.open("https://railway.app/new")
    time.sleep(2)
    
    # فتح Render كبديل
    print("🌟 فتح Render كبديل...")
    webbrowser.open("https://render.com")
    
    print("✅ تم فتح كلا الخيارين")

def show_quick_fix():
    """عرض الحل السريع"""
    print("⚡ الحل السريع:")
    print("=" * 40)
    print()
    print("🎯 اختر أحد الخيارين:")
    print()
    print("أ) إصلاح Railway الحالي:")
    print("   1. تحقق من Build Logs")
    print("   2. أضف متغيرات البيئة")
    print("   3. أضف PostgreSQL")
    print("   4. أعد النشر")
    print()
    print("ب) نشر جديد على Render:")
    print("   1. أسرع وأسهل")
    print("   2. مجاني تماماً")
    print("   3. يعمل بشكل مضمون")
    print("   4. جاهز في 10 دقائق")
    print()

def get_user_choice():
    """الحصول على اختيار المستخدم"""
    print("🤔 أي حل تفضل؟")
    print("1️⃣ إصلاح Railway الحالي")
    print("2️⃣ نشر جديد على Render (موصى به)")
    print("3️⃣ نشر جديد على Railway")
    print()
    
    choice = input("اختر رقم (1-3): ").strip()
    
    if choice == "1":
        print("\n🔧 اتبع خطوات إصلاح Railway أعلاه")
        return "railway_fix"
    elif choice == "2":
        print("\n🌟 ممتاز! Render هو الخيار الأفضل للمبتدئين")
        return "render_new"
    elif choice == "3":
        print("\n🚀 نشر جديد على Railway")
        return "railway_new"
    else:
        print("\n❌ اختيار غير صحيح، سأختار Render (الأفضل)")
        return "render_new"

def show_render_steps():
    """عرض خطوات Render المفصلة"""
    print("\n📋 خطوات Render المفصلة:")
    print("=" * 50)
    print()
    print("1️⃣ في صفحة Render:")
    print("   - انقر 'Get Started for Free'")
    print("   - سجل دخول بـ GitHub")
    print()
    print("2️⃣ إنشاء Web Service:")
    print("   - انقر 'New +'")
    print("   - اختر 'Web Service'")
    print("   - اختر 'Build and deploy from Git repository'")
    print()
    print("3️⃣ ربط المشروع:")
    print("   - ابحث عن 'math-competition-platform'")
    print("   - انقر 'Connect'")
    print()
    print("4️⃣ إعدادات الخدمة:")
    print("   Name: math-competition-platform")
    print("   Environment: Python 3")
    print("   Build Command: pip install -r requirements.txt")
    print("   Start Command: gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT")
    print()
    print("5️⃣ متغيرات البيئة:")
    print("   DJANGO_SECRET_KEY = django-insecure-render-production-key-2025")
    print("   DEBUG = False")
    print("   ALLOWED_HOSTS = *.onrender.com")
    print()
    print("6️⃣ إنشاء قاعدة البيانات:")
    print("   - New + > PostgreSQL")
    print("   - انسخ External Database URL")
    print("   - أضفه كـ DATABASE_URL في Web Service")
    print()
    print("7️⃣ النشر:")
    print("   - انقر 'Create Web Service'")
    print("   - انتظر 10-15 دقيقة")
    print("   - احصل على الرابط")
    print()

def main():
    """الدالة الرئيسية"""
    print_header()
    diagnose_problem()
    show_railway_fix()
    show_render_alternative()
    show_quick_fix()
    
    # فتح صفحات الحلول
    open_solutions()
    
    # الحصول على اختيار المستخدم
    choice = get_user_choice()
    
    if choice == "render_new":
        show_render_steps()
        print("\n🎉 Render مفتوح ومستعد!")
        print("🎯 اتبع الخطوات أعلاه وستحصل على مشروعك في 15 دقيقة")
    
    print("\n" + "=" * 60)
    print("💡 نصيحة: Render أسهل وأكثر استقراراً للمبتدئين")
    print("🚀 Railway أسرع لكن يحتاج خبرة أكثر")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  تم إيقاف العملية")
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
    
    input("\n⏸️  اضغط Enter للخروج...")
