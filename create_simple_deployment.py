#!/usr/bin/env python3
"""
إنشاء نشر بسيط بدون nixpacks.toml
Create simple deployment without nixpacks.toml
"""

import os
import zipfile
import shutil
from datetime import datetime

def create_simple_deployment():
    """إنشاء نشر بسيط"""
    
    # إنشاء مجلد جديد
    simple_folder = f"railway_simple_deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(simple_folder, exist_ok=True)
    
    print(f"📦 إنشاء النشر البسيط: {simple_folder}")
    
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
        dest_path = os.path.join(simple_folder, item)
        
        if os.path.exists(source_path):
            if os.path.isdir(source_path):
                shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                print(f"✅ نسخ مجلد: {item}")
            else:
                shutil.copy2(source_path, dest_path)
                print(f"✅ نسخ ملف: {item}")
    
    # نسخ railway.json المحدث
    shutil.copy2('railway.json', os.path.join(simple_folder, 'railway.json'))
    print("✅ نسخ railway.json المحدث")
    
    # إنشاء Procfile بسيط
    procfile_content = "web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT"
    
    with open(os.path.join(simple_folder, 'Procfile'), 'w') as f:
        f.write(procfile_content)
    print("✅ إنشاء Procfile")
    
    # إنشاء runtime.txt لتحديد إصدار Python
    runtime_content = "python-3.11.0"
    
    with open(os.path.join(simple_folder, 'runtime.txt'), 'w') as f:
        f.write(runtime_content)
    print("✅ إنشاء runtime.txt")
    
    # إنشاء ملف .env للمرجع
    env_content = """# متغيرات البيئة لـ Railway (أضفها يدوياً في Variables)
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
    
    with open(os.path.join(simple_folder, '.env.example'), 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("✅ إنشاء .env.example")
    
    # إنشاء ملف مضغوط
    zip_filename = f"{simple_folder}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(simple_folder):
            # تجاهل مجلدات __pycache__
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                # تجاهل ملفات .pyc
                if not file.endswith('.pyc'):
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, simple_folder)
                    zipf.write(file_path, arc_name)
    
    print(f"✅ إنشاء ملف مضغوط: {zip_filename}")
    
    # عرض محتويات railway.json
    print("\n📋 محتوى railway.json:")
    with open(os.path.join(simple_folder, 'railway.json'), 'r') as f:
        content = f.read()
        print(content)
    
    # إحصائيات الملف المضغوط
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        file_count = len(zipf.namelist())
    
    file_size = os.path.getsize(zip_filename) / 1024 / 1024
    
    print(f"\n📊 إحصائيات:")
    print(f"📁 عدد الملفات: {file_count}")
    print(f"📦 حجم الملف: {file_size:.2f} MB")
    
    return simple_folder, zip_filename

if __name__ == "__main__":
    folder, zip_file = create_simple_deployment()
    
    print("\n" + "="*50)
    print("🎉 النشر البسيط جاهز!")
    print("="*50)
    print(f"📁 المجلد: {folder}")
    print(f"📦 الملف المضغوط: {zip_file}")
    
    print("\n🔧 الميزات:")
    print("✅ بدون nixpacks.toml (تجنب مشاكل التنسيق)")
    print("✅ railway.json محدث مع WSGI صحيح")
    print("✅ Procfile بسيط وواضح")
    print("✅ runtime.txt لتحديد Python 3.11")
    print("✅ جميع ملفات المشروع")
    
    print("\n🚀 الخطوات التالية:")
    print("1️⃣ احذف المشروع الحالي في Railway")
    print("2️⃣ أنشئ مشروع جديد")
    print(f"3️⃣ ارفع الملف: {zip_file}")
    print("4️⃣ أضف PostgreSQL")
    print("5️⃣ أضف متغيرات البيئة يدوياً:")
    print("   WSGI_APPLICATION=alhassan.wsgi.application")
    print("   DJANGO_SETTINGS_MODULE=alhassan.settings")
    print("   DEBUG=False")
    print("6️⃣ احصل على الرابط الدائم!")
    
    print("\n🎯 هذا الحل أبسط وأكثر موثوقية!")
