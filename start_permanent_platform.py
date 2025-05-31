#!/usr/bin/env python3
"""
🚀 بدء تشغيل المنصة الدائمة
Start permanent platform
"""

import subprocess
import sys
import os
import time

def check_requirements():
    """فحص المتطلبات"""
    print("🔍 فحص المتطلبات...")
    
    # فحص Python
    if sys.version_info < (3, 7):
        print("❌ يتطلب Python 3.7 أو أحدث")
        return False
    
    print(f"✅ Python {sys.version}")
    
    # فحص Django
    try:
        import django
        print(f"✅ Django {django.get_version()}")
    except ImportError:
        print("❌ Django غير مثبت")
        return False
    
    # فحص ngrok
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ ngrok متوفر")
        else:
            print("❌ ngrok غير متوفر")
            return False
    except FileNotFoundError:
        print("❌ ngrok غير مثبت")
        return False
    
    return True

def install_missing_requirements():
    """تثبيت المتطلبات المفقودة"""
    print("📦 تثبيت المتطلبات...")
    
    try:
        # تثبيت متطلبات Python
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ تم تثبيت متطلبات Python")
        
        # تثبيت ngrok إذا لم يكن مثبت
        try:
            subprocess.run(['ngrok', 'version'], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("📦 تثبيت ngrok...")
            subprocess.run([sys.executable, "install_ngrok.py"], check=True)
        
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

def create_startup_script():
    """إنشاء سكريبت بدء التشغيل"""
    
    if os.name == 'nt':  # Windows
        script_content = '''@echo off
echo 🚀 بدء تشغيل منصة المسابقات الرياضية
echo =====================================

cd /d "%~dp0"
python start_permanent_platform.py

pause
'''
        with open("start_platform.bat", "w", encoding='utf-8') as f:
            f.write(script_content)
        print("✅ تم إنشاء start_platform.bat")
    
    else:  # Linux/Mac
        script_content = '''#!/bin/bash
echo "🚀 بدء تشغيل منصة المسابقات الرياضية"
echo "====================================="

cd "$(dirname "$0")"
python3 start_permanent_platform.py

read -p "اضغط Enter للمتابعة..."
'''
        with open("start_platform.sh", "w", encoding='utf-8') as f:
            f.write(script_content)
        
        # جعل الملف قابل للتنفيذ
        os.chmod("start_platform.sh", 0o755)
        print("✅ تم إنشاء start_platform.sh")

def display_instructions():
    """عرض التعليمات"""
    print("\n" + "="*60)
    print("📋 تعليمات التشغيل")
    print("="*60)
    print("🎯 المنصة جاهزة للتشغيل الدائم!")
    print()
    print("🚀 طرق التشغيل:")
    if os.name == 'nt':  # Windows
        print("   • انقر مرتين على start_platform.bat")
        print("   • أو شغل: python permanent_deploy.py")
    else:  # Linux/Mac
        print("   • شغل: ./start_platform.sh")
        print("   • أو شغل: python3 permanent_deploy.py")
    
    print()
    print("🔗 بعد التشغيل ستحصل على:")
    print("   • رابط دائم للمنصة")
    print("   • مراقبة تلقائية للخدمات")
    print("   • إعادة تشغيل تلقائي عند الحاجة")
    print()
    print("📄 ملفات مهمة:")
    print("   • PERMANENT_DEPLOYMENT_INFO.txt - معلومات النشر")
    print("   • deployment_status.json - حالة النشر")
    print("   • ngrok.log - سجل ngrok")
    print()
    print("⚠️ ملاحظات:")
    print("   • احتفظ بالنافذة مفتوحة للتشغيل الدائم")
    print("   • اضغط Ctrl+C لإيقاف المنصة")
    print("   • للحصول على أفضل أداء، أنشئ حساب ngrok مجاني")
    print("="*60)

def main():
    """الدالة الرئيسية"""
    print("🎯 إعداد منصة المسابقات الرياضية للتشغيل الدائم")
    print("="*60)
    
    # فحص المتطلبات
    if not check_requirements():
        print("\n📦 تثبيت المتطلبات المفقودة...")
        if not install_missing_requirements():
            print("❌ فشل في تثبيت المتطلبات")
            return False
    
    # إعداد Django
    if not setup_django():
        print("❌ فشل في إعداد Django")
        return False
    
    # إنشاء سكريبت البدء
    create_startup_script()
    
    # عرض التعليمات
    display_instructions()
    
    # سؤال المستخدم عن التشغيل الفوري
    choice = input("\n❓ هل تريد تشغيل المنصة الآن؟ (y/n): ").lower().strip()
    
    if choice in ['y', 'yes', 'نعم', '1']:
        print("\n🚀 بدء تشغيل المنصة...")
        try:
            subprocess.run([sys.executable, "permanent_deploy.py"])
        except KeyboardInterrupt:
            print("\n✅ تم إيقاف المنصة")
    else:
        print("\n✅ الإعداد مكتمل! يمكنك تشغيل المنصة لاحقاً")
    
    return True

if __name__ == "__main__":
    main()
