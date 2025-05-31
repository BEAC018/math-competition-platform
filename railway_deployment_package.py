#!/usr/bin/env python3
"""
إنشاء حزمة نشر محدثة لـ Railway
Create updated deployment package for Railway
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_railway_package():
    """إنشاء حزمة نشر محدثة"""
    
    # إنشاء مجلد جديد
    package_name = f"railway_fixed_deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(package_name, exist_ok=True)
    
    print(f"📦 إنشاء حزمة النشر المحدثة: {package_name}")
    
    # نسخ الملفات الأساسية
    files_to_copy = [
        'manage.py',
        'requirements.txt',
        'alhassan/',
        'competitions/',
        'static/',
        'templates/',
        'db.sqlite3'
    ]
    
    for item in files_to_copy:
        if os.path.exists(item):
            dest_path = os.path.join(package_name, item)
            if os.path.isdir(item):
                shutil.copytree(item, dest_path, dirs_exist_ok=True)
                print(f"✅ نسخ مجلد: {item}")
            else:
                shutil.copy2(item, dest_path)
                print(f"✅ نسخ ملف: {item}")
    
    # نسخ ملف nixpacks.toml الجديد
    if os.path.exists('nixpacks.toml'):
        shutil.copy2('nixpacks.toml', os.path.join(package_name, 'nixpacks.toml'))
        print("✅ نسخ nixpacks.toml")
    
    # إنشاء Procfile محدث
    procfile_content = "web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT"
    
    with open(os.path.join(package_name, 'Procfile'), 'w') as f:
        f.write(procfile_content)
    print("✅ إنشاء Procfile محدث")
    
    # إنشاء ملف .env للمرجع
    env_content = """# متغيرات البيئة لـ Railway
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
    
    with open(os.path.join(package_name, '.env.example'), 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("✅ إنشاء .env.example")
    
    # إنشاء تعليمات النشر
    instructions = f"""# 🚀 تعليمات النشر المحدثة لـ Railway

## 📦 الحزمة: {package_name}

### 🔧 الإصلاحات المطبقة:
✅ إضافة ملف nixpacks.toml مع إعدادات WSGI
✅ تحديث Procfile مع gunicorn
✅ إعدادات متغيرات البيئة الصحيحة
✅ إعدادات قاعدة البيانات PostgreSQL

### 🚀 خطوات النشر:

#### 1️⃣ في Railway:
- احذف المشروع الحالي أو أنشئ مشروع جديد
- اختر "Deploy from GitHub" أو "Upload files"

#### 2️⃣ رفع الملفات:
- ارفع جميع ملفات هذا المجلد
- أو ارفع الملف المضغوط

#### 3️⃣ إضافة قاعدة البيانات:
- أضف PostgreSQL من قائمة الخدمات
- سيتم ربطها تلقائياً

#### 4️⃣ متغيرات البيئة (اختيارية):
إذا لم تعمل nixpacks.toml، أضف هذه المتغيرات يدوياً:

```
WSGI_APPLICATION=alhassan.wsgi.application
DJANGO_SETTINGS_MODULE=alhassan.settings
SECRET_KEY=django-insecure-math-platform-railway-2024-xyz123
DEBUG=False
ALLOWED_HOSTS=.railway.app,.up.railway.app,localhost,127.0.0.1
PORT=8000
```

### 🎯 النتيجة المتوقعة:
```
🌐 الرابط الدائم: https://your-project.up.railway.app/student/login/
🔑 رمز الدخول: ben25
```

### 🆘 في حالة المشاكل:
1. تحقق من Build Logs
2. تأكد من وجود ملف nixpacks.toml
3. تحقق من متغيرات البيئة
4. تأكد من اتصال قاعدة البيانات

### 📱 رسالة للمشاركة (بعد النشر):
```
🎯 منصة المسابقات الرياضية - الرابط الدائم

🌐 الرابط: [ضع رابطك هنا]/student/login/
🔑 رمز الدخول: ben25

📝 خطوات الدخول:
1. انقر الرابط
2. اكتب اسمك
3. اكتب الرمز: ben25
4. اختر مستواك
5. ابدأ المسابقة!

🎮 استمتعوا! 🚀
```

## ✅ الملفات المتضمنة:
- nixpacks.toml (إعدادات النشر)
- Procfile (أمر التشغيل)
- .env.example (متغيرات البيئة)
- جميع ملفات المشروع

## 🎊 الحزمة جاهزة للنشر!
"""
    
    with open(os.path.join(package_name, 'DEPLOYMENT_INSTRUCTIONS.md'), 'w', encoding='utf-8') as f:
        f.write(instructions)
    print("✅ إنشاء تعليمات النشر")
    
    # إنشاء ملف مضغوط
    zip_filename = f"{package_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_name):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, package_name)
                zipf.write(file_path, arc_name)
    
    print(f"✅ إنشاء ملف مضغوط: {zip_filename}")
    
    print("\n" + "="*50)
    print("🎉 تم إنشاء حزمة النشر المحدثة بنجاح!")
    print("="*50)
    print(f"📁 المجلد: {package_name}")
    print(f"🗜️ الملف المضغوط: {zip_filename}")
    print("📋 التعليمات: DEPLOYMENT_INSTRUCTIONS.md")
    
    print("\n🚀 الخطوات التالية:")
    print("1️⃣ احذف المشروع الحالي في Railway")
    print("2️⃣ أنشئ مشروع جديد")
    print("3️⃣ ارفع الملف المضغوط")
    print("4️⃣ أضف PostgreSQL")
    print("5️⃣ احصل على الرابط الدائم!")
    
    return package_name, zip_filename

if __name__ == "__main__":
    create_railway_package()
