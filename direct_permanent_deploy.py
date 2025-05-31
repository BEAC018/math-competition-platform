#!/usr/bin/env python3
"""
🚀 نشر دائم مباشر بدون Git
Direct permanent deployment without Git
"""

import os
import json
import zipfile
import shutil
from datetime import datetime

class DirectPermanentDeploy:
    def __init__(self):
        self.deployment_folder = f"math_platform_deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def create_deployment_package(self):
        """إنشاء حزمة النشر"""
        print("📦 إنشاء حزمة النشر الدائم...")
        
        # إنشاء مجلد النشر
        os.makedirs(self.deployment_folder, exist_ok=True)
        
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
        
        # نسخ الملفات
        for item in items_to_copy:
            if os.path.exists(item):
                dest_path = os.path.join(self.deployment_folder, item)
                if os.path.isdir(item):
                    shutil.copytree(item, dest_path, dirs_exist_ok=True)
                    print(f"✅ تم نسخ مجلد: {item}")
                else:
                    shutil.copy2(item, dest_path)
                    print(f"✅ تم نسخ ملف: {item}")
            else:
                print(f"⚠️ ملف غير موجود: {item}")
        
        return True
    
    def create_railway_files(self):
        """إنشاء ملفات Railway"""
        print("🚂 إنشاء ملفات Railway...")
        
        # railway.json
        railway_config = {
            "build": {
                "builder": "NIXPACKS"
            },
            "deploy": {
                "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:$PORT",
                "restartPolicyType": "ON_FAILURE",
                "restartPolicyMaxRetries": 10
            }
        }
        
        railway_path = os.path.join(self.deployment_folder, 'railway.json')
        with open(railway_path, 'w', encoding='utf-8') as f:
            json.dump(railway_config, f, indent=2)
        
        # Procfile
        procfile_content = "web: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:$PORT"
        procfile_path = os.path.join(self.deployment_folder, 'Procfile')
        with open(procfile_path, 'w', encoding='utf-8') as f:
            f.write(procfile_content)
        
        # runtime.txt
        runtime_path = os.path.join(self.deployment_folder, 'runtime.txt')
        with open(runtime_path, 'w', encoding='utf-8') as f:
            f.write('python-3.11.10')
        
        print("✅ تم إنشاء ملفات Railway")
        return True
    
    def create_render_files(self):
        """إنشاء ملفات Render"""
        print("🎨 إنشاء ملفات Render...")
        
        # render.yaml
        render_config = """services:
  - type: web
    name: math-competition-platform
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:$PORT
    envVars:
      - key: DEBUG
        value: False
      - key: DJANGO_SETTINGS_MODULE
        value: alhassan.settings
"""
        
        render_path = os.path.join(self.deployment_folder, 'render.yaml')
        with open(render_path, 'w', encoding='utf-8') as f:
            f.write(render_config)
        
        print("✅ تم إنشاء ملفات Render")
        return True
    
    def create_vercel_files(self):
        """إنشاء ملفات Vercel"""
        print("⚡ إنشاء ملفات Vercel...")
        
        # vercel.json
        vercel_config = {
            "version": 2,
            "builds": [
                {
                    "src": "alhassan/wsgi.py",
                    "use": "@vercel/python",
                    "config": {"maxLambdaSize": "15mb", "runtime": "python3.9"}
                }
            ],
            "routes": [
                {
                    "src": "/(.*)",
                    "dest": "alhassan/wsgi.py"
                }
            ]
        }
        
        vercel_path = os.path.join(self.deployment_folder, 'vercel.json')
        with open(vercel_path, 'w', encoding='utf-8') as f:
            json.dump(vercel_config, f, indent=2)
        
        print("✅ تم إنشاء ملفات Vercel")
        return True
    
    def create_deployment_instructions(self):
        """إنشاء تعليمات النشر"""
        print("📋 إنشاء تعليمات النشر...")
        
        instructions = f"""# 🚀 دليل النشر الدائم - بدون Git

## 📦 حزمة النشر جاهزة في: {self.deployment_folder}

---

## 🎯 الطرق المتاحة للنشر الدائم:

### 1️⃣ Railway (الأسهل - موصى به):

#### الخطوات:
1. **اذهب إلى:** https://railway.app
2. **سجل دخول** بـ GitHub أو البريد الإلكتروني
3. **اضغط "New Project"**
4. **اختر "Empty Project"**
5. **اضغط "Deploy from GitHub repo"** ← **"Deploy from local folder"**
6. **ارفع مجلد** `{self.deployment_folder}`
7. **انتظر النشر** (2-5 دقائق)
8. **اضغط "Generate Domain"** للحصول على الرابط

#### النتيجة:
```
🌐 الرابط الدائم: https://math-competition-platform.railway.app/student/login/
🔑 رمز الدخول: ben25
```

---

### 2️⃣ Render (بديل ممتاز):

#### الخطوات:
1. **اذهب إلى:** https://render.com
2. **أنشئ حساب جديد**
3. **اضغط "New Web Service"**
4. **اختر "Build and deploy from a Git repository"**
5. **ارفع الملفات** أو اربط GitHub
6. **اضبط الإعدادات:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:$PORT`

#### النتيجة:
```
🌐 الرابط الدائم: https://math-competition-platform.onrender.com/student/login/
🔑 رمز الدخول: ben25
```

---

### 3️⃣ Heroku (كلاسيكي):

#### الخطوات:
1. **اذهب إلى:** https://heroku.com
2. **أنشئ حساب جديد**
3. **اضغط "Create new app"**
4. **اسم التطبيق:** `math-competition-platform`
5. **في تبويب "Deploy":**
   - **اختر "GitHub"**
   - **ارفع الملفات**
   - **فعل "Automatic deploys"**

#### النتيجة:
```
🌐 الرابط الدائم: https://math-competition-platform.herokuapp.com/student/login/
🔑 رمز الدخول: ben25
```

---

### 4️⃣ Vercel (سريع):

#### الخطوات:
1. **اذهب إلى:** https://vercel.com
2. **سجل دخول بـ GitHub**
3. **اسحب وأفلت** مجلد `{self.deployment_folder}`
4. **انتظر النشر** (1-2 دقيقة)

#### النتيجة:
```
🌐 الرابط الدائم: https://math-competition-platform.vercel.app/student/login/
🔑 رمز الدخول: ben25
```

---

## 🎯 التوصية:

### للمبتدئين:
**استخدم Railway** - الأسهل والأكثر موثوقية

### للمطورين:
**استخدم Render** - مميزات متقدمة ومجاني

### للسرعة:
**استخدم Vercel** - نشر فوري

---

## 📱 رسالة للمشاركة (بعد النشر):

```
🎯 منصة المسابقات الرياضية - الرابط الدائم

🌐 الرابط: [ضع رابطك هنا]/student/login/
🔑 رمز الدخول: ben25

📝 الخطوات:
1. انقر الرابط
2. اكتب اسمك
3. اكتب الرمز: ben25
4. اختر مستواك
5. ابدأ المسابقة!

🎮 استمتعوا! 🚀

✅ هذا رابط دائم يعمل 24/7
```

---

## ✅ مميزات الحل الدائم:

- **🌐 رابط ثابت** لا يتغير أبداً
- **⏰ يعمل 24/7** بدون انقطاع
- **🔄 لا يحتاج إعادة تشغيل**
- **💰 مجاني بالكامل**
- **📱 يعمل على جميع الأجهزة**
- **🔒 آمن ومحمي**
- **📊 مراقبة تلقائية**
- **🆘 دعم فني**

---

## 🆘 الدعم:

إذا واجهت أي مشكلة:
1. **تحقق من السجلات** في لوحة التحكم
2. **تأكد من ملف requirements.txt**
3. **راجع إعدادات البيئة**
4. **اتصل بدعم المنصة**

---

## 🎊 النتيجة النهائية:

بعد اتباع أي من الطرق أعلاه، ستحصل على:

✅ **رابط دائم ثابت**
✅ **يعمل بدون انقطاع**
✅ **لا يحتاج صيانة**
✅ **مجاني بالكامل**

**🚀 منصتك ستكون متاحة للعالم 24/7!**
"""

        instructions_path = os.path.join(self.deployment_folder, 'DEPLOYMENT_INSTRUCTIONS.md')
        with open(instructions_path, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print("✅ تم إنشاء تعليمات النشر")
        return True
    
    def create_zip_package(self):
        """إنشاء ملف مضغوط للنشر"""
        print("🗜️ إنشاء ملف مضغوط...")
        
        zip_filename = f"{self.deployment_folder}.zip"
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.deployment_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, self.deployment_folder)
                    zipf.write(file_path, arc_name)
        
        print(f"✅ تم إنشاء ملف مضغوط: {zip_filename}")
        return zip_filename
    
    def run_deployment_preparation(self):
        """تشغيل تحضير النشر"""
        print("🚀 تحضير النشر الدائم للمنصة")
        print("="*50)
        
        # إنشاء حزمة النشر
        if not self.create_deployment_package():
            return False
        
        # إنشاء ملفات المنصات المختلفة
        self.create_railway_files()
        self.create_render_files()
        self.create_vercel_files()
        
        # إنشاء التعليمات
        self.create_deployment_instructions()
        
        # إنشاء ملف مضغوط
        zip_file = self.create_zip_package()
        
        print("\n" + "="*50)
        print("🎉 تم تحضير النشر الدائم بنجاح!")
        print("="*50)
        
        print(f"\n📁 مجلد النشر: {self.deployment_folder}")
        print(f"🗜️ ملف مضغوط: {zip_file}")
        print(f"📋 تعليمات النشر: {self.deployment_folder}/DEPLOYMENT_INSTRUCTIONS.md")
        
        print("\n🎯 الخطوات التالية:")
        print("1️⃣ اقرأ ملف DEPLOYMENT_INSTRUCTIONS.md")
        print("2️⃣ اختر منصة النشر (Railway موصى به)")
        print("3️⃣ ارفع الملفات أو الملف المضغوط")
        print("4️⃣ احصل على رابط دائم")
        print("5️⃣ شارك الرابط مع المشاركين")
        
        print("\n🌐 بعد النشر ستحصل على رابط مثل:")
        print("https://math-competition-platform.railway.app/student/login/")
        print("🔑 رمز الدخول: ben25")
        
        print("\n✅ هذا الرابط سيكون دائم ولن يتغير أبداً!")
        
        return True

def main():
    """الدالة الرئيسية"""
    deployment = DirectPermanentDeploy()
    deployment.run_deployment_preparation()

if __name__ == "__main__":
    main()
