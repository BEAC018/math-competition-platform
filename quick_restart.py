#!/usr/bin/env python3
"""
🚀 إعادة تشغيل سريع مع الإعدادات المحدثة
Quick restart with updated settings
"""

import subprocess
import sys
import time

def restart_with_current_url():
    """إعادة تشغيل مع الرابط الحالي"""
    print("🔄 إعادة تشغيل المنصة مع الإعدادات المحدثة...")
    
    try:
        # تشغيل الخادم مباشرة
        print("🚀 تشغيل خادم Django...")
        subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
    except KeyboardInterrupt:
        print("\n✅ تم إيقاف الخادم")

def show_current_info():
    """عرض معلومات الرابط الحالي"""
    print("📋 معلومات المنصة الحالية:")
    print("="*50)
    print("🌐 الرابط: https://482e-105-157-119-224.ngrok-free.app")
    print("👥 للتلاميذ: https://482e-105-157-119-224.ngrok-free.app/student/login/")
    print("👨‍🏫 للأساتذة: https://482e-105-157-119-224.ngrok-free.app/accounts/login/")
    print("🔑 رمز الدخول: ben25")
    print("="*50)

def main():
    """الدالة الرئيسية"""
    print("🎯 منصة المسابقات الرياضية - إعادة تشغيل سريع")
    print("="*55)
    
    show_current_info()
    
    print("\n✅ تم إصلاح مشكلة CSRF")
    print("🔧 الإعدادات محدثة لدعم ngrok")
    print("🎯 المنصة جاهزة للاستخدام!")
    
    restart_with_current_url()

if __name__ == "__main__":
    main()
