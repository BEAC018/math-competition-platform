#!/usr/bin/env python3
"""
🚀 نشر بسيط ومباشر
Simple Direct Deployment
"""

import subprocess
import sys
import os
import time

def install_requirements():
    """تثبيت المتطلبات"""
    print("📦 تثبيت المتطلبات...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ تم تثبيت المتطلبات")
        return True
    except Exception as e:
        print(f"❌ خطأ في تثبيت المتطلبات: {e}")
        return False

def setup_django():
    """إعداد Django"""
    print("🔧 إعداد Django...")
    try:
        # تطبيق قاعدة البيانات
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("✅ تم إعداد قاعدة البيانات")
        
        # جمع الملفات الثابتة
        subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
        print("✅ تم جمع الملفات الثابتة")
        
        return True
    except Exception as e:
        print(f"❌ خطأ في إعداد Django: {e}")
        return False

def create_ngrok_tunnel():
    """إنشاء نفق ngrok"""
    try:
        from pyngrok import ngrok
        
        print("🌐 إنشاء رابط عام...")
        public_url = ngrok.connect(8000)
        
        # استخراج الرابط النظيف
        clean_url = str(public_url).split('"')[1]
        
        print("\n" + "="*60)
        print("🎉 تم إنشاء الرابط العام بنجاح!")
        print("="*60)
        print(f"🌐 الرابط العام: {clean_url}")
        print(f"👥 رابط التلاميذ: {clean_url}/student/login/")
        print(f"👨‍🏫 رابط الأساتذة: {clean_url}/accounts/login/")
        print(f"🔑 رمز دخول التلاميذ: ben25")
        print("="*60)
        
        # حفظ الروابط
        with open("LIVE_URLS.txt", "w", encoding='utf-8') as f:
            f.write("🌐 روابط المنصة المباشرة\n")
            f.write("="*30 + "\n\n")
            f.write(f"الرابط الرئيسي: {clean_url}\n")
            f.write(f"رابط التلاميذ: {clean_url}/student/login/\n")
            f.write(f"رابط الأساتذة: {clean_url}/accounts/login/\n")
            f.write(f"رمز الدخول: ben25\n\n")
            f.write("📱 رسالة للتلاميذ:\n")
            f.write("-"*20 + "\n")
            f.write("🎯 منصة المسابقات الرياضية\n\n")
            f.write(f"🌐 الرابط: {clean_url}/student/login/\n")
            f.write("🔑 رمز الدخول: ben25\n\n")
            f.write("📝 التعليمات:\n")
            f.write("1. انقر على الرابط\n")
            f.write("2. اكتب اسمك الكامل\n")
            f.write("3. اكتب الرمز: ben25\n")
            f.write("4. اختر مستواك الدراسي\n")
            f.write("5. ابدأ المسابقة!\n\n")
            f.write("🎮 استمتعوا بالتعلم! 🚀\n")
        
        print("📄 تم حفظ الروابط في ملف LIVE_URLS.txt")
        
        return clean_url
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء الرابط العام: {e}")
        return None

def start_server():
    """تشغيل الخادم"""
    print("🚀 تشغيل الخادم...")
    try:
        subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
    except KeyboardInterrupt:
        print("\n✅ تم إيقاف الخادم")

def main():
    """الدالة الرئيسية"""
    print("🎯 نشر منصة المسابقات الرياضية")
    print("="*40)
    
    # تثبيت المتطلبات
    if not install_requirements():
        return
    
    # إعداد Django
    if not setup_django():
        return
    
    # إنشاء رابط عام
    public_url = create_ngrok_tunnel()
    
    if public_url:
        print("\n🎯 المنصة جاهزة للاستخدام!")
        print("📋 شارك الروابط مع التلاميذ والأساتذة")
        print("⏹️ اضغط Ctrl+C لإيقاف الخادم")
        
        # تشغيل الخادم
        start_server()
    else:
        print("\n❌ فشل في إنشاء الرابط العام")
        print("💡 يمكنك تشغيل الخادم محلياً:")
        print("   python manage.py runserver 0.0.0.0:8000")

if __name__ == "__main__":
    main()
