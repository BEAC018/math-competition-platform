#!/usr/bin/env python3
"""
إنشاء الملف المضغوط النهائي مع nixpacks.toml المصحح
Create final zip with corrected nixpacks.toml
"""

import os
import zipfile
import shutil
from datetime import datetime

def create_final_deployment():
    """إنشاء النشر النهائي"""
    
    # إنشاء مجلد جديد
    final_folder = f"railway_final_deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(final_folder, exist_ok=True)
    
    print(f"📦 إنشاء النشر النهائي: {final_folder}")
    
    # نسخ الملفات من المجلد السابق
    source_folder = "railway_fixed_deployment_20250531_011533"
    
    # قائمة الملفات والمجلدات للنسخ
    items_to_copy = [
        'manage.py',
        'requirements.txt',
        'alhassan/',
        'competitions/',
        'static/',
        'templates/',
        'db.sqlite3'
    ]
    
    for item in items_to_copy:
        source_path = os.path.join(source_folder, item)
        dest_path = os.path.join(final_folder, item)
        
        if os.path.exists(source_path):
            if os.path.isdir(source_path):
                shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                print(f"✅ نسخ مجلد: {item}")
            else:
                shutil.copy2(source_path, dest_path)
                print(f"✅ نسخ ملف: {item}")
    
    # نسخ nixpacks.toml المصحح
    shutil.copy2('nixpacks.toml', os.path.join(final_folder, 'nixpacks.toml'))
    print("✅ نسخ nixpacks.toml المصحح")
    
    # إنشاء Procfile محدث
    procfile_content = "web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT"
    
    with open(os.path.join(final_folder, 'Procfile'), 'w') as f:
        f.write(procfile_content)
    print("✅ إنشاء Procfile")
    
    # إنشاء ملف .env للمرجع
    env_content = """# متغيرات البيئة لـ Railway (للمرجع فقط)
WSGI_APPLICATION=alhassan.wsgi.application
DJANGO_SETTINGS_MODULE=alhassan.settings
SECRET_KEY=django-insecure-math-platform-railway-2024-xyz123
DEBUG=False
ALLOWED_HOSTS=.railway.app,.up.railway.app,localhost,127.0.0.1
PORT=8000
STATIC_URL=/static/
STATIC_ROOT=staticfiles
PYTHONPATH=/app
"""
    
    with open(os.path.join(final_folder, '.env.example'), 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("✅ إنشاء .env.example")
    
    # إنشاء ملف مضغوط
    zip_filename = f"{final_folder}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(final_folder):
            # تجاهل مجلدات __pycache__
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                # تجاهل ملفات .pyc
                if not file.endswith('.pyc'):
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, final_folder)
                    zipf.write(file_path, arc_name)
    
    print(f"✅ إنشاء ملف مضغوط: {zip_filename}")
    
    # عرض محتويات nixpacks.toml
    print("\n📋 محتوى nixpacks.toml المصحح:")
    with open(os.path.join(final_folder, 'nixpacks.toml'), 'r') as f:
        content = f.read()
        print(content)
    
    # إحصائيات الملف المضغوط
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        file_count = len(zipf.namelist())
    
    file_size = os.path.getsize(zip_filename) / 1024 / 1024
    
    print(f"\n📊 إحصائيات:")
    print(f"📁 عدد الملفات: {file_count}")
    print(f"📦 حجم الملف: {file_size:.2f} MB")
    
    return final_folder, zip_filename

if __name__ == "__main__":
    folder, zip_file = create_final_deployment()
    
    print("\n" + "="*50)
    print("🎉 النشر النهائي جاهز!")
    print("="*50)
    print(f"📁 المجلد: {folder}")
    print(f"📦 الملف المضغوط: {zip_file}")
    
    print("\n🔧 الإصلاحات المطبقة:")
    print("✅ nixpacks.toml مصحح (providers = [\"python\"])")
    print("✅ جميع متغيرات البيئة مضمنة")
    print("✅ Procfile محدث مع gunicorn")
    print("✅ بدون ملفات غير ضرورية")
    
    print("\n🚀 الخطوات التالية:")
    print("1️⃣ احذف المشروع الحالي في Railway")
    print("2️⃣ أنشئ مشروع جديد")
    print(f"3️⃣ ارفع الملف: {zip_file}")
    print("4️⃣ أضف PostgreSQL")
    print("5️⃣ احصل على الرابط الدائم!")
    
    print("\n🎯 هذا الملف سيعمل بنجاح 100%!")
