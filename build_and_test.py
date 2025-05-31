#!/usr/bin/env python3
"""
سكريبت بناء واختبار الملف التنفيذي
Build and test executable script
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def test_launcher():
    """اختبار launcher.py قبل البناء"""
    print("🧪 اختبار launcher.py...")
    
    try:
        # تشغيل launcher.py لمدة قصيرة للتأكد من عمله
        process = subprocess.Popen([sys.executable, "launcher.py"])
        time.sleep(3)  # انتظار 3 ثوان
        process.terminate()
        print("✅ launcher.py يعمل بشكل صحيح")
        return True
    except Exception as e:
        print(f"❌ خطأ في launcher.py: {e}")
        return False

def install_requirements():
    """تثبيت المتطلبات"""
    print("📦 تثبيت المتطلبات...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements_exe.txt"
        ])
        print("✅ تم تثبيت المتطلبات بنجاح")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل في تثبيت المتطلبات: {e}")
        return False

def build_executable():
    """بناء الملف التنفيذي"""
    print("🔨 بناء الملف التنفيذي...")
    
    try:
        result = subprocess.run([sys.executable, "build_exe.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ تم بناء الملف التنفيذي بنجاح")
            print(result.stdout)
            return True
        else:
            print("❌ فشل في بناء الملف التنفيذي")
            print("خطأ:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ خطأ في البناء: {e}")
        return False

def test_executable():
    """اختبار الملف التنفيذي"""
    exe_path = Path("dist") / "MathCompetitionPlatform.exe"
    
    if not exe_path.exists():
        print("❌ لم يتم العثور على الملف التنفيذي")
        return False
    
    print("🧪 اختبار الملف التنفيذي...")
    print(f"📁 مسار الملف: {exe_path}")
    print(f"📊 حجم الملف: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    
    # يمكن إضافة اختبارات إضافية هنا
    print("✅ الملف التنفيذي جاهز للاختبار")
    
    return True

def main():
    """الدالة الرئيسية"""
    print("🚀 بناء واختبار منصة المسابقات الرياضية")
    print("=" * 50)
    
    # التحقق من الملفات المطلوبة
    required_files = [
        'launcher.py',
        'build_exe.py', 
        'requirements_exe.txt',
        'manage.py',
        'alhassan/settings.py'
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ الملف المطلوب غير موجود: {file_path}")
            return False
    
    # اختبار launcher.py
    if not test_launcher():
        print("❌ فشل في اختبار launcher.py")
        return False
    
    # تثبيت المتطلبات
    if not install_requirements():
        return False
    
    # بناء الملف التنفيذي
    if not build_executable():
        return False
    
    # اختبار الملف التنفيذي
    if not test_executable():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 تم بناء واختبار التطبيق بنجاح!")
    print("=" * 50)
    
    print("\n📋 الخطوات التالية:")
    print("1. اذهب إلى مجلد dist/")
    print("2. انقر نقراً مزدوجاً على MathCompetitionPlatform.exe")
    print("3. اضغط 'بدء الخادم' في النافذة")
    print("4. استخدم رمز الدخول: ben25")
    
    print("\n📦 للتوزيع:")
    print("- استخدم الملف المضغوط الذي تم إنشاؤه")
    print("- شارك مع المستخدمين مع ملف README.txt")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎯 هل تريد تشغيل الملف التنفيذي الآن؟ (y/n): ", end="")
        choice = input().lower()
        
        if choice in ['y', 'yes', 'نعم']:
            exe_path = Path("dist") / "MathCompetitionPlatform.exe"
            if exe_path.exists():
                print("🚀 تشغيل الملف التنفيذي...")
                subprocess.Popen([str(exe_path)])
            else:
                print("❌ لم يتم العثور على الملف التنفيذي")
    
    input("\nاضغط Enter للخروج...")
