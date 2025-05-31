#!/usr/bin/env python3
"""
🌐 الحصول على رابط عام للمنصة
Get public URL for the platform
"""

import subprocess
import time
import threading
import os
import sys

def start_django_server():
    """تشغيل خادم Django"""
    print("🚀 تشغيل خادم Django...")
    try:
        subprocess.run([
            sys.executable, "manage.py", "runserver", "0.0.0.0:8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n✅ تم إيقاف الخادم")
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")

def setup_ngrok():
    """إعداد ngrok للحصول على رابط عام"""
    print("🔧 إعداد ngrok...")
    
    try:
        # تثبيت pyngrok
        subprocess.run([sys.executable, "-m", "pip", "install", "pyngrok"], check=True)
        print("✅ تم تثبيت pyngrok")
        
        from pyngrok import ngrok
        
        # إنشاء نفق عام
        print("🌐 إنشاء رابط عام...")
        public_url = ngrok.connect(8000)
        
        print("\n" + "="*50)
        print("🎉 تم إنشاء الرابط العام بنجاح!")
        print("="*50)
        print(f"🌐 الرابط العام: {public_url}")
        print(f"👥 رابط التلاميذ: {public_url}/student/login/")
        print(f"👨‍🏫 رابط الأساتذة: {public_url}/accounts/login/")
        print(f"🔑 رمز دخول التلاميذ: ben25")
        print("="*50)
        
        # حفظ الرابط في ملف
        with open("public_url.txt", "w", encoding='utf-8') as f:
            f.write(f"الرابط العام: {public_url}\n")
            f.write(f"رابط التلاميذ: {public_url}/student/login/\n")
            f.write(f"رابط الأساتذة: {public_url}/accounts/login/\n")
            f.write(f"رمز الدخول: ben25\n")
        
        print("📄 تم حفظ الروابط في ملف public_url.txt")
        
        return str(public_url)
        
    except ImportError:
        print("❌ فشل في تثبيت pyngrok")
        return None
    except Exception as e:
        print(f"❌ خطأ في إعداد ngrok: {e}")
        return None

def create_simple_server():
    """إنشاء خادم بسيط مع عرض الرابط"""
    print("🔧 إعداد الخادم...")
    
    # تشغيل الإعدادات
    try:
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
        print("✅ تم إعداد Django")
    except Exception as e:
        print(f"❌ خطأ في إعداد Django: {e}")
        return
    
    # محاولة استخدام ngrok
    public_url = setup_ngrok()
    
    if public_url:
        # تشغيل Django في خيط منفصل
        django_thread = threading.Thread(target=start_django_server)
        django_thread.daemon = True
        django_thread.start()
        
        print("\n🎯 المنصة جاهزة للاستخدام!")
        print("⏹️ اضغط Ctrl+C لإيقاف الخادم")
        
        try:
            # إبقاء البرنامج يعمل
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n✅ تم إيقاف الخادم")
    else:
        print("\n📋 تعليمات بديلة:")
        print("1️⃣ في Replit، اضغط زر 'Run'")
        print("2️⃣ ابحث عن أيقونة 🌐 في الأعلى")
        print("3️⃣ أو ابحث عن تبويب 'Webview'")
        print("4️⃣ انسخ الرابط الذي يظهر")

def show_replit_instructions():
    """عرض تعليمات Replit"""
    print("\n📋 تعليمات الحصول على الرابط في Replit:")
    print("="*50)
    print("1️⃣ اضغط زر 'Run' الأخضر")
    print("2️⃣ انتظر حتى يبدأ الخادم")
    print("3️⃣ ابحث عن واحد من هذه:")
    print("   • نافذة صغيرة تظهر في الأعلى")
    print("   • أيقونة 🌐 في الشريط العلوي")
    print("   • تبويب 'Webview' أو 'Output'")
    print("   • رسالة في Console تحتوي على رابط")
    print("4️⃣ انسخ الرابط")
    print("5️⃣ أضف '/student/login/' للتلاميذ")
    print("="*50)

def main():
    """الدالة الرئيسية"""
    print("🌐 الحصول على رابط عام لمنصة المسابقات الرياضية")
    print("="*50)
    
    # التحقق من البيئة
    if "REPL_SLUG" in os.environ:
        print("🔍 تم اكتشاف بيئة Replit")
        show_replit_instructions()
        
        choice = input("\n❓ هل تريد المحاولة مع ngrok؟ (y/n): ").lower()
        if choice in ['y', 'yes', 'نعم']:
            create_simple_server()
        else:
            print("✅ اتبع التعليمات أعلاه للحصول على الرابط")
    else:
        print("🔍 بيئة محلية - سيتم استخدام ngrok")
        create_simple_server()

if __name__ == "__main__":
    main()
