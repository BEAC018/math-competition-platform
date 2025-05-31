#!/usr/bin/env python3
"""
📦 تثبيت ngrok تلقائياً
Automatic ngrok installation
"""

import subprocess
import sys
import os
import platform
import requests
import zipfile
import shutil
from pathlib import Path

def check_ngrok_installed():
    """فحص ما إذا كان ngrok مثبت"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ ngrok مثبت بالفعل: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ ngrok غير مثبت")
    return False

def install_ngrok_windows():
    """تثبيت ngrok على Windows"""
    print("📦 تثبيت ngrok على Windows...")
    
    try:
        # تحميل ngrok
        url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
        print("⬇️ تحميل ngrok...")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # حفظ الملف
        zip_path = "ngrok.zip"
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("📂 استخراج ngrok...")
        
        # استخراج الملف
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # حذف ملف الضغط
        os.remove(zip_path)
        
        # إضافة ngrok للمسار
        current_dir = os.getcwd()
        ngrok_path = os.path.join(current_dir, "ngrok.exe")
        
        if os.path.exists(ngrok_path):
            print("✅ تم تثبيت ngrok بنجاح")
            return True
        else:
            print("❌ فشل في تثبيت ngrok")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في تثبيت ngrok: {e}")
        return False

def install_ngrok_linux():
    """تثبيت ngrok على Linux"""
    print("📦 تثبيت ngrok على Linux...")
    
    try:
        # محاولة التثبيت عبر snap
        result = subprocess.run(['snap', 'install', 'ngrok'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ تم تثبيت ngrok عبر snap")
            return True
        
        # محاولة التحميل المباشر
        url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
        print("⬇️ تحميل ngrok...")
        
        subprocess.run(['wget', url, '-O', 'ngrok.tgz'], check=True)
        subprocess.run(['tar', 'xzf', 'ngrok.tgz'], check=True)
        subprocess.run(['sudo', 'mv', 'ngrok', '/usr/local/bin/'], check=True)
        subprocess.run(['rm', 'ngrok.tgz'], check=True)
        
        print("✅ تم تثبيت ngrok بنجاح")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تثبيت ngrok: {e}")
        return False

def install_ngrok_mac():
    """تثبيت ngrok على macOS"""
    print("📦 تثبيت ngrok على macOS...")
    
    try:
        # محاولة التثبيت عبر Homebrew
        result = subprocess.run(['brew', 'install', 'ngrok/ngrok/ngrok'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ تم تثبيت ngrok عبر Homebrew")
            return True
        
        # محاولة التحميل المباشر
        url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip"
        print("⬇️ تحميل ngrok...")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open("ngrok.zip", 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        subprocess.run(['unzip', 'ngrok.zip'], check=True)
        subprocess.run(['sudo', 'mv', 'ngrok', '/usr/local/bin/'], check=True)
        subprocess.run(['rm', 'ngrok.zip'], check=True)
        
        print("✅ تم تثبيت ngrok بنجاح")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تثبيت ngrok: {e}")
        return False

def install_python_requirements():
    """تثبيت متطلبات Python"""
    print("📦 تثبيت متطلبات Python...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        print("✅ تم تثبيت متطلبات Python")
        return True
    except Exception as e:
        print(f"❌ خطأ في تثبيت متطلبات Python: {e}")
        return False

def setup_ngrok_account():
    """إرشادات إعداد حساب ngrok"""
    print("\n" + "="*50)
    print("🔐 إعداد حساب ngrok")
    print("="*50)
    print("📋 للحصول على أفضل أداء، يُنصح بإنشاء حساب مجاني:")
    print()
    print("1️⃣ اذهب إلى: https://ngrok.com/signup")
    print("2️⃣ أنشئ حساب مجاني")
    print("3️⃣ اذهب إلى: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("4️⃣ انسخ التوكن")
    print("5️⃣ شغل الأمر: ngrok config add-authtoken YOUR_TOKEN")
    print()
    print("💡 بدون حساب: ستعمل المنصة لكن مع قيود زمنية")
    print("✅ مع حساب مجاني: ستعمل المنصة بدون قيود")
    print("="*50)

def main():
    """الدالة الرئيسية"""
    print("🎯 إعداد ngrok لمنصة المسابقات الرياضية")
    print("="*50)
    
    # فحص ما إذا كان ngrok مثبت
    if check_ngrok_installed():
        setup_ngrok_account()
        return True
    
    # تثبيت متطلبات Python
    if not install_python_requirements():
        return False
    
    # تحديد نظام التشغيل وتثبيت ngrok
    system = platform.system().lower()
    
    if system == "windows":
        success = install_ngrok_windows()
    elif system == "linux":
        success = install_ngrok_linux()
    elif system == "darwin":  # macOS
        success = install_ngrok_mac()
    else:
        print(f"❌ نظام التشغيل غير مدعوم: {system}")
        return False
    
    if success:
        print("\n🎉 تم تثبيت ngrok بنجاح!")
        setup_ngrok_account()
        return True
    else:
        print("\n❌ فشل في تثبيت ngrok")
        print("💡 يمكنك تثبيته يدوياً من: https://ngrok.com/download")
        return False

if __name__ == "__main__":
    main()
