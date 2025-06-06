#!/usr/bin/env python3
"""
🖥️ تشغيل منصة المسابقات الرياضية محلياً
Local startup for math competition platform
"""

import subprocess
import sys
import webbrowser
import time
import os

def main():
    print("🖥️ منصة المسابقات الرياضية - التشغيل المحلي")
    print("=" * 50)
    print()
    
    try:
        # تحضير قاعدة البيانات
        print("📊 تحضير قاعدة البيانات...")
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        
        # تجميع الملفات الثابتة
        print("📁 تجميع الملفات الثابتة...")
        subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
        
        print()
        print("🚀 بدء تشغيل الخادم المحلي...")
        print("🌐 الرابط: http://localhost:8000")
        print("👥 رابط التلاميذ: http://localhost:8000/student/login/")
        print("👨‍🏫 رابط الأساتذة: http://localhost:8000/accounts/login/")
        print("🔑 رمز دخول التلاميذ: ben25")
        print()
        print("⏹️ لإيقاف الخادم: اضغط Ctrl+C")
        print("=" * 50)
        print()
        
        # انتظار قليل ثم فتح المتصفح
        time.sleep(2)
        try:
            webbrowser.open('http://localhost:8000')
            print("🌐 تم فتح المتصفح تلقائياً")
        except:
            print("📋 افتح المتصفح يدوياً على: http://localhost:8000")
        
        print()
        
        # تشغيل Django
        subprocess.run([sys.executable, "manage.py", "runserver"])
        
    except KeyboardInterrupt:
        print("\n✅ تم إيقاف الخادم")
    except Exception as e:
        print(f"❌ خطأ: {e}")
        input("اضغط Enter للخروج...")

if __name__ == "__main__":
    main()
