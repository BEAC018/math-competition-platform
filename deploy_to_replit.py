#!/usr/bin/env python3
"""
🚀 نشر على Replit مباشرة
Deploy directly to Replit
"""

import subprocess
import sys
import os

def setup_replit_files():
    """إعداد ملفات Replit"""
    print("📁 إعداد ملفات Replit...")
    
    # ملف .replit
    replit_content = '''run = "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"
language = "python3"

[nix]
channel = "stable-22_11"

[deployment]
run = ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
deploymentTarget = "cloudrun"

[env]
PYTHONPATH = "${REPL_HOME}:${PYTHONPATH}"
DJANGO_SETTINGS_MODULE = "alhassan.settings"'''

    with open('.replit', 'w', encoding='utf-8') as f:
        f.write(replit_content)
    
    print("✅ تم إنشاء ملف .replit")

def create_local_server():
    """تشغيل خادم محلي"""
    print("🚀 تشغيل خادم محلي...")
    
    try:
        # إعداد Django
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
        
        print("\n" + "="*60)
        print("🎯 الخادم المحلي جاهز!")
        print("="*60)
        print("🌐 الرابط المحلي: http://localhost:8000")
        print("👥 للتلاميذ: http://localhost:8000/student/login/")
        print("👨‍🏫 للأساتذة: http://localhost:8000/accounts/login/")
        print("🔑 رمز الدخول: ben25")
        print("="*60)
        print("📋 لمشاركة المنصة:")
        print("1️⃣ ارفع المشروع على Replit")
        print("2️⃣ اضغط زر 'Run' في Replit")
        print("3️⃣ ستحصل على رابط عام")
        print("="*60)
        
        # تشغيل الخادم
        subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
        
    except KeyboardInterrupt:
        print("\n✅ تم إيقاف الخادم")
    except Exception as e:
        print(f"❌ خطأ: {e}")

def create_deployment_guide():
    """إنشاء دليل النشر"""
    guide_content = """# 🚀 دليل نشر منصة المسابقات الرياضية

## 📋 الطرق المتاحة للنشر:

### 1️⃣ Replit (الأسهل - موصى به)
1. اذهب إلى https://replit.com
2. أنشئ حساب جديد أو سجل دخول
3. اضغط "Create Repl"
4. اختر "Import from GitHub" أو "Upload folder"
5. ارفع ملفات المشروع
6. اضغط زر "Run" الأخضر
7. ستحصل على رابط عام تلقائياً

### 2️⃣ Railway
1. اذهب إلى https://railway.app
2. سجل دخول بـ GitHub
3. اضغط "New Project"
4. اختر "Deploy from GitHub repo"
5. اختر المشروع
6. سيتم النشر تلقائياً

### 3️⃣ Render
1. اذهب إلى https://render.com
2. أنشئ حساب جديد
3. اضغط "New Web Service"
4. اربط GitHub
5. اختر المشروع
6. اضبط الإعدادات وانشر

### 4️⃣ Heroku
1. اذهب إلى https://heroku.com
2. أنشئ حساب جديد
3. اضغط "Create new app"
4. اربط GitHub
5. اختر المشروع
6. فعل "Automatic deploys"

## 🔗 روابط المنصة بعد النشر:
- **للتلاميذ:** [رابطك]/student/login/
- **للأساتذة:** [رابطك]/accounts/login/
- **رمز الدخول:** ben25

## 📱 رسالة للمشاركة:
```
🎯 منصة المسابقات الرياضية

🌐 الرابط: [ضع رابطك هنا]/student/login/
🔑 رمز الدخول: ben25

📝 الخطوات:
1. انقر الرابط
2. اكتب اسمك
3. اكتب الرمز: ben25
4. اختر مستواك
5. ابدأ المسابقة!

🎮 استمتعوا بالتعلم! 🚀
```

## ✅ المنصة جاهزة للنشر!
"""

    with open("DEPLOYMENT_GUIDE.md", "w", encoding='utf-8') as f:
        f.write(guide_content)
    
    print("📄 تم إنشاء دليل النشر: DEPLOYMENT_GUIDE.md")

def main():
    """الدالة الرئيسية"""
    print("🎯 إعداد منصة المسابقات الرياضية للنشر")
    print("="*55)
    
    # إعداد ملفات Replit
    setup_replit_files()
    
    # إنشاء دليل النشر
    create_deployment_guide()
    
    print("\n✅ تم إعداد المنصة للنشر!")
    print("📋 اختر إحدى الطرق التالية:")
    print("1️⃣ تشغيل محلي للاختبار")
    print("2️⃣ نشر على Replit")
    print("3️⃣ نشر على منصة أخرى")
    
    choice = input("\n❓ اختر (1/2/3): ").strip()
    
    if choice == "1":
        create_local_server()
    elif choice == "2":
        print("\n📋 تعليمات Replit:")
        print("1. اذهب إلى https://replit.com")
        print("2. أنشئ Repl جديد")
        print("3. ارفع ملفات المشروع")
        print("4. اضغط 'Run'")
        print("5. ستحصل على رابط عام!")
    else:
        print("\n📄 تحقق من ملف DEPLOYMENT_GUIDE.md للتعليمات الكاملة")

if __name__ == "__main__":
    main()
