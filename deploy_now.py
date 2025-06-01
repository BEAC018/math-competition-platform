#!/usr/bin/env python3
"""
🚀 نشر فوري لمنصة المسابقات الرياضية
سيقوم هذا السكريبت بنشر المشروع فوراً على Railway
"""

import webbrowser
import time

def print_banner():
    """طباعة شعار البرنامج"""
    print("=" * 60)
    print("🚀 نشر فوري لمنصة المسابقات الرياضية على Railway")
    print("=" * 60)
    print()

def deploy_to_railway():
    """النشر المباشر على Railway"""
    print("🌐 فتح صفحة Railway للنشر المباشر...")
    
    # رابط النشر المباشر من GitHub
    github_repo = "BEAC1/math-competition-platform"
    railway_url = f"https://railway.app/new/template?template=https://github.com/{github_repo}"
    
    print(f"🔗 فتح الرابط: {railway_url}")
    webbrowser.open(railway_url)
    
    return railway_url

def show_instructions():
    """عرض التعليمات المفصلة"""
    print("\n📋 اتبع هذه الخطوات في صفحة Railway:")
    print("=" * 60)
    print()
    print("1️⃣ سجل دخول بـ GitHub")
    print("   - انقر 'Login with GitHub'")
    print("   - وافق على الصلاحيات")
    print()
    print("2️⃣ انشر المشروع")
    print("   - انقر 'Deploy Now'")
    print("   - انتظر 3-5 دقائق")
    print()
    print("3️⃣ أضف قاعدة بيانات")
    print("   - انقر 'New Service'")
    print("   - اختر 'Database'")
    print("   - اختر 'PostgreSQL'")
    print("   - انتظر دقيقة واحدة")
    print()
    print("4️⃣ أضف متغيرات البيئة")
    print("   - اذهب إلى Variables tab")
    print("   - أضف:")
    print("     DJANGO_SECRET_KEY = django-insecure-railway-production-key-2025")
    print("     DEBUG = False")
    print("     ALLOWED_HOSTS = *.railway.app,*.up.railway.app")
    print()
    print("5️⃣ احصل على الرابط")
    print("   - اذهب إلى Settings tab")
    print("   - انقر 'Generate Domain'")
    print("   - انسخ الرابط")
    print()

def show_usage():
    """عرض كيفية الاستخدام"""
    print("📱 كيفية استخدام المنصة:")
    print("=" * 60)
    print()
    print("🎓 للطلاب:")
    print("   الرابط: https://your-app.railway.app/student/login/")
    print("   الرمز: ben25")
    print("   الخطوات:")
    print("   1. يفتحون الرابط")
    print("   2. يدخلون الرمز ben25")
    print("   3. يكتبون اسمهم")
    print("   4. يختارون مستواهم الدراسي")
    print("   5. يبدأون المسابقة")
    print()
    print("👨‍🏫 للمعلمين:")
    print("   الرابط: https://your-app.railway.app/accounts/login/")
    print("   الخطوات:")
    print("   1. يفتحون الرابط")
    print("   2. يسجلون دخول أو ينشئون حساب")
    print("   3. يديرون المشاركين والمسابقات")
    print("   4. يطلعون على الإحصائيات")
    print()

def get_project_url():
    """الحصول على رابط المشروع"""
    print("⏳ انتظار اكتمال النشر...")
    print("=" * 60)
    
    input("\n⏸️  اضغط Enter بعد اكتمال النشر على Railway...")
    
    print("\n🔗 أدخل رابط مشروعك من Railway:")
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
            f.write(f"🏢 منصة الاستضافة: Railway\n")
        
        print("💾 تم حفظ الرابط في LIVE_PROJECT_URL.txt")
        
        # اختبار الرابط
        print(f"\n🧪 فتح الرابط للاختبار...")
        webbrowser.open(project_url)
        
        return project_url
    
    return None

def show_success(project_url):
    """عرض رسالة النجاح"""
    print("\n" + "=" * 60)
    print("🎉 تم النشر بنجاح!")
    print("=" * 60)
    print()
    print(f"🌐 مشروعك متاح على: {project_url}")
    print(f"🎓 للطلاب: {project_url}/student/login/")
    print(f"👨‍🏫 للمعلمين: {project_url}/accounts/login/")
    print()
    print("📤 شارك الرابط مع:")
    print("   - الطلاب للمشاركة في المسابقات")
    print("   - المعلمين لإدارة المنصة")
    print("   - المجتمعات التعليمية")
    print()
    print("🎯 استمتع بمشروعك على الإنترنت!")
    print("=" * 60)

def main():
    """الدالة الرئيسية"""
    print_banner()
    
    # النشر على Railway
    railway_url = deploy_to_railway()
    
    # عرض التعليمات
    show_instructions()
    show_usage()
    
    # الحصول على رابط المشروع
    project_url = get_project_url()
    
    if project_url:
        show_success(project_url)
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
    
    input("\n⏸️  اضغط Enter للخروج...")
