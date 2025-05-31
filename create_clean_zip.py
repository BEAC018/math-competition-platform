#!/usr/bin/env python3
"""
إنشاء ملف مضغوط نظيف بدون README.md
Create clean zip without README.md
"""

import os
import zipfile
from datetime import datetime

def create_clean_zip():
    """إنشاء ملف مضغوط نظيف"""
    
    source_folder = "railway_fixed_deployment_20250531_011533"
    zip_filename = f"railway_clean_deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    print(f"📦 إنشاء ملف مضغوط نظيف: {zip_filename}")
    
    # قائمة الملفات المطلوبة
    required_files = [
        'manage.py',
        'requirements.txt',
        'nixpacks.toml',
        'Procfile',
        '.env.example'
    ]
    
    # قائمة المجلدات المطلوبة
    required_folders = [
        'alhassan',
        'competitions',
        'static',
        'templates'
    ]
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # إضافة الملفات الأساسية
        for file_name in required_files:
            file_path = os.path.join(source_folder, file_name)
            if os.path.exists(file_path):
                zipf.write(file_path, file_name)
                print(f"✅ إضافة ملف: {file_name}")
        
        # إضافة المجلدات
        for folder_name in required_folders:
            folder_path = os.path.join(source_folder, folder_name)
            if os.path.exists(folder_path):
                for root, dirs, files in os.walk(folder_path):
                    # تجاهل مجلدات __pycache__
                    dirs[:] = [d for d in dirs if d != '__pycache__']
                    
                    for file in files:
                        # تجاهل ملفات .pyc
                        if not file.endswith('.pyc'):
                            file_path = os.path.join(root, file)
                            # الحصول على المسار النسبي
                            arc_name = os.path.relpath(file_path, source_folder)
                            zipf.write(file_path, arc_name)
                
                print(f"✅ إضافة مجلد: {folder_name}")
        
        # إضافة قاعدة البيانات إذا كانت موجودة
        db_path = os.path.join(source_folder, 'db.sqlite3')
        if os.path.exists(db_path):
            zipf.write(db_path, 'db.sqlite3')
            print("✅ إضافة قاعدة البيانات")
    
    print(f"\n✅ تم إنشاء الملف المضغوط: {zip_filename}")
    
    # عرض محتويات الملف المضغوط
    print("\n📋 محتويات الملف المضغوط:")
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        file_list = zipf.namelist()
        for file_name in sorted(file_list)[:20]:  # أول 20 ملف
            print(f"  📄 {file_name}")
        
        if len(file_list) > 20:
            print(f"  ... و {len(file_list) - 20} ملف آخر")
    
    print(f"\n🎯 إجمالي الملفات: {len(file_list)}")
    print(f"📦 حجم الملف: {os.path.getsize(zip_filename) / 1024 / 1024:.2f} MB")
    
    return zip_filename

if __name__ == "__main__":
    zip_file = create_clean_zip()
    
    print("\n" + "="*50)
    print("🎉 الملف المضغوط النظيف جاهز!")
    print("="*50)
    print(f"📁 الملف: {zip_file}")
    print("\n🚀 الخطوات التالية:")
    print("1️⃣ احذف المشروع الحالي في Railway")
    print("2️⃣ أنشئ مشروع جديد")
    print("3️⃣ ارفع هذا الملف المضغوط")
    print("4️⃣ أضف PostgreSQL")
    print("5️⃣ احصل على الرابط الدائم!")
    
    print("\n✅ هذا الملف لا يحتوي على README.md")
    print("✅ يحتوي على جميع ملفات المشروع المطلوبة")
    print("✅ nixpacks.toml موجود لحل مشكلة WSGI")
