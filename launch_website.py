#!/usr/bin/env python3
"""
🚀 إطلاق الموقع تلقائياً
سيقوم هذا السكريبت بإطلاق الموقع على Render بالكامل
"""

import webbrowser
import time
import subprocess
import os

def print_launch_banner():
    """طباعة شعار الإطلاق"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║           🚀 إطلاق منصة المسابقات الرياضية                ║
    ║                                                              ║
    ║                  سأتولى كل شيء بنفسي                       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def prepare_for_launch():
    """تحضير الملفات للإطلاق"""
    print("⚙️  تحضير الملفات للإطلاق...")
    
    # التحقق من الملفات المطلوبة
    required_files = ['render.yaml', 'requirements.txt', 'manage.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} موجود")
        else:
            print(f"❌ {file} مفقود")
            return False
    
    print("✅ جميع الملفات جاهزة")
    return True

def commit_changes():
    """حفظ التغييرات في Git"""
    print("📤 حفظ التغييرات في Git...")
    try:
        git_cmd = r"C:\Program Files\Git\bin\git.exe"
        
        # إضافة الملفات
        subprocess.run([git_cmd, 'add', '.'], check=True, capture_output=True)
        
        # إنشاء commit
        commit_msg = "deploy: إطلاق الموقع على Render مع render.yaml"
        subprocess.run([git_cmd, 'commit', '-m', commit_msg], check=True, capture_output=True)
        
        # رفع إلى GitHub
        subprocess.run([git_cmd, 'push', 'origin', 'main'], check=True, capture_output=True)
        
        print("✅ تم حفظ ورفع التغييرات بنجاح")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  تعذر حفظ التغييرات (قد تكون محفوظة مسبقاً)")
        return True
    except Exception as e:
        print(f"❌ خطأ في Git: {e}")
        return False

def launch_render():
    """إطلاق Render"""
    print("🌐 إطلاق Render للنشر التلقائي...")
    
    # رابط النشر المباشر مع render.yaml
    render_url = "https://render.com/deploy?repo=https://github.com/BEAC1/math-competition-platform"
    
    print(f"🔗 فتح الرابط: {render_url}")
    webbrowser.open(render_url)
    
    return render_url

def show_launch_instructions():
    """عرض تعليمات الإطلاق"""
    print("\n" + "=" * 60)
    print("📋 تعليمات الإطلاق التلقائي:")
    print("=" * 60)
    print()
    print("🎯 في صفحة Render المفتوحة:")
    print()
    print("1️⃣ سجل دخول بـ GitHub (30 ثانية)")
    print("   - انقر 'Connect with GitHub'")
    print("   - وافق على الصلاحيات")
    print()
    print("2️⃣ النشر التلقائي (5 دقائق)")
    print("   - سيتم اكتشاف render.yaml تلقائياً")
    print("   - انقر 'Apply' لتطبيق الإعدادات")
    print("   - انقر 'Create Web Service'")
    print("   - انتظر اكتمال البناء")
    print()
    print("3️⃣ إنشاء قاعدة البيانات (2 دقيقة)")
    print("   - سيتم إنشاؤها تلقائياً من render.yaml")
    print("   - أو انقر 'New +' > 'PostgreSQL' يدوياً")
    print()
    print("4️⃣ الحصول على الرابط (فوري)")
    print("   - سيظهر الرابط في Dashboard")
    print("   - مثال: https://math-competition-platform.onrender.com")
    print()

def show_expected_result():
    """عرض النتيجة المتوقعة"""
    print("🎊 النتيجة المتوقعة:")
    print("=" * 40)
    print()
    print("🌐 رابط الموقع:")
    print("   https://math-competition-platform.onrender.com")
    print()
    print("🎓 للطلاب:")
    print("   https://math-competition-platform.onrender.com/student/login/")
    print("   الرمز: ben25")
    print()
    print("👨‍🏫 للمعلمين:")
    print("   https://math-competition-platform.onrender.com/accounts/login/")
    print()
    print("⏱️  الوقت المتوقع: 10-15 دقيقة")
    print("💰 التكلفة: مجاني تماماً")
    print("🔒 الأمان: SSL مجاني (HTTPS)")
    print()

def monitor_deployment():
    """مراقبة النشر"""
    print("⏳ مراقبة النشر...")
    print("=" * 40)
    
    input("\n⏸️  اضغط Enter بعد اكتمال النشر في Render...")
    
    print("\n🔗 أدخل رابط موقعك من Render:")
    website_url = input("الرابط: ").strip()
    
    if website_url:
        if not website_url.startswith('http'):
            website_url = 'https://' + website_url
        
        print(f"\n🎊 مبروك! موقعك متاح على: {website_url}")
        
        # حفظ الرابط
        with open('LIVE_WEBSITE_URL.txt', 'w', encoding='utf-8') as f:
            f.write(f"🌐 رابط الموقع المباشر: {website_url}\n")
            f.write(f"🎓 رابط الطلاب: {website_url}/student/login/\n")
            f.write(f"👨‍🏫 رابط المعلمين: {website_url}/accounts/login/\n")
            f.write(f"🔑 رمز دخول الطلاب: ben25\n")
            f.write(f"📅 تاريخ الإطلاق: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"🏢 منصة الاستضافة: Render\n")
            f.write(f"💰 نوع الاستضافة: مجانية\n")
        
        print("💾 تم حفظ الرابط في LIVE_WEBSITE_URL.txt")
        
        # اختبار الموقع
        print(f"\n🧪 فتح الموقع للاختبار...")
        webbrowser.open(website_url)
        
        return website_url
    
    return None

def show_success_message(website_url):
    """عرض رسالة النجاح"""
    success_banner = f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                  🎉 تم إطلاق الموقع بنجاح! 🎉              ║
    ║                                                              ║
    ║  موقعك متاح الآن للعالم على الإنترنت                      ║
    ║                                                              ║
    ║  🌐 الرابط: {website_url:<43} ║
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
    print_launch_banner()
    
    # تحضير الملفات
    if not prepare_for_launch():
        print("❌ فشل في تحضير الملفات")
        return
    
    # حفظ التغييرات
    if not commit_changes():
        print("❌ فشل في حفظ التغييرات")
        return
    
    # إطلاق Render
    render_url = launch_render()
    
    # عرض التعليمات
    show_launch_instructions()
    show_expected_result()
    
    # مراقبة النشر
    website_url = monitor_deployment()
    
    if website_url:
        show_success_message(website_url)
        
        print("\n🎯 الخطوات التالية:")
        print("1. اختبر الموقع مع بعض الطلاب")
        print("2. شارك الرابط مع المعلمين")
        print("3. راقب الاستخدام والإحصائيات")
        print("4. استمتع بنجاح مشروعك!")
    else:
        print("\n⚠️  لم يتم إدخال رابط الموقع")
        print("💡 يمكنك إضافة الرابط لاحقاً في ملف LIVE_WEBSITE_URL.txt")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  تم إيقاف العملية")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
    
    input("\n⏸️  اضغط Enter للخروج...")
