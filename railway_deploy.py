#!/usr/bin/env python3
"""
🚂 نشر دائم على Railway
Permanent deployment on Railway
"""

import subprocess
import sys
import os
import json
import time
import webbrowser

class RailwayDeployment:
    def __init__(self):
        self.project_name = "math-competition-platform"
        self.github_repo = None
        
    def check_requirements(self):
        """فحص المتطلبات"""
        print("🔍 فحص المتطلبات...")
        
        # فحص Git
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Git متوفر")
            else:
                print("❌ Git غير مثبت")
                return False
        except FileNotFoundError:
            print("❌ Git غير مثبت")
            print("📦 حمل Git من: https://git-scm.com/download")
            return False
        
        # فحص ملفات المشروع
        required_files = ['manage.py', 'requirements.txt', 'alhassan/settings.py']
        for file in required_files:
            if not os.path.exists(file):
                print(f"❌ ملف مفقود: {file}")
                return False
        
        print("✅ جميع المتطلبات متوفرة")
        return True
    
    def prepare_for_deployment(self):
        """تحضير المشروع للنشر"""
        print("📦 تحضير المشروع للنشر...")
        
        # إنشاء ملف railway.json
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
        
        with open('railway.json', 'w', encoding='utf-8') as f:
            json.dump(railway_config, f, indent=2)
        
        print("✅ تم إنشاء railway.json")
        
        # تحديث Procfile
        procfile_content = "web: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:$PORT"
        
        with open('Procfile', 'w', encoding='utf-8') as f:
            f.write(procfile_content)
        
        print("✅ تم تحديث Procfile")
        
        # إنشاء ملف .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Deployment
staticfiles/
.railway/
"""
        
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        print("✅ تم إنشاء .gitignore")
        
        return True
    
    def setup_git_repo(self):
        """إعداد مستودع Git"""
        print("📂 إعداد مستودع Git...")
        
        try:
            # تهيئة Git إذا لم يكن موجود
            if not os.path.exists('.git'):
                subprocess.run(['git', 'init'], check=True)
                print("✅ تم تهيئة مستودع Git")
            
            # إضافة الملفات
            subprocess.run(['git', 'add', '.'], check=True)
            
            # إنشاء commit
            subprocess.run(['git', 'commit', '-m', 'Initial commit for Railway deployment'], check=True)
            
            print("✅ تم إنشاء commit")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ خطأ في Git: {e}")
            return False
    
    def create_deployment_guide(self):
        """إنشاء دليل النشر"""
        guide_content = """# 🚂 دليل النشر الدائم على Railway

## 🎯 الخطوات للحصول على رابط دائم:

### 1️⃣ إنشاء حساب GitHub:
1. اذهب إلى: https://github.com
2. أنشئ حساب جديد (مجاني)
3. تأكد من تفعيل البريد الإلكتروني

### 2️⃣ رفع المشروع على GitHub:
1. اذهب إلى: https://github.com/new
2. اسم المستودع: `math-competition-platform`
3. اختر "Public"
4. اضغط "Create repository"

### 3️⃣ رفع الملفات:
```bash
# في مجلد المشروع، شغل:
git remote add origin https://github.com/YOUR_USERNAME/math-competition-platform.git
git branch -M main
git push -u origin main
```

### 4️⃣ النشر على Railway:
1. اذهب إلى: https://railway.app
2. اضغط "Login with GitHub"
3. اضغط "New Project"
4. اختر "Deploy from GitHub repo"
5. اختر مستودع `math-competition-platform`
6. اضغط "Deploy Now"

### 5️⃣ الحصول على الرابط:
1. انتظر انتهاء النشر (2-5 دقائق)
2. اضغط على المشروع
3. اذهب إلى تبويب "Settings"
4. اضغط "Generate Domain"
5. ستحصل على رابط مثل: `https://math-competition-platform.railway.app`

## 🎉 النتيجة النهائية:

### 🌐 الرابط الدائم:
```
https://math-competition-platform.railway.app/student/login/
```

### 🔑 رمز الدخول:
```
ben25
```

### ✅ المميزات:
- رابط ثابت لا يتغير أبداً
- يعمل 24/7 بدون انقطاع
- لا يحتاج إعادة تشغيل
- مجاني بالكامل
- دعم فني من Railway

## 📱 رسالة للمشاركة:
```
🎯 منصة المسابقات الرياضية - الرابط الدائم

🌐 الرابط: https://math-competition-platform.railway.app/student/login/
🔑 رمز الدخول: ben25

📝 الخطوات:
1. انقر الرابط
2. اكتب اسمك
3. اكتب الرمز: ben25
4. اختر مستواك
5. ابدأ المسابقة!

🎮 استمتعوا! 🚀

ملاحظة: هذا رابط دائم يعمل 24/7
```

## 🔧 إدارة المشروع:
- **تحديث الكود:** ارفع التغييرات على GitHub وسيتم النشر تلقائياً
- **مراقبة الحالة:** من لوحة تحكم Railway
- **عرض السجلات:** من تبويب "Logs" في Railway

## 🆘 الدعم:
- **Railway:** https://docs.railway.app
- **GitHub:** https://docs.github.com
"""

        with open('RAILWAY_DEPLOYMENT_GUIDE.md', 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print("✅ تم إنشاء دليل النشر: RAILWAY_DEPLOYMENT_GUIDE.md")
    
    def create_alternative_solutions(self):
        """إنشاء حلول بديلة"""
        alternatives_content = """# 🌐 الحلول البديلة للنشر الدائم

## 1️⃣ Render (مجاني):
1. اذهب إلى: https://render.com
2. اربط GitHub
3. اختر "Web Service"
4. الرابط: `https://math-competition-platform.onrender.com`

## 2️⃣ Vercel (مجاني):
1. اذهب إلى: https://vercel.com
2. اربط GitHub
3. نشر تلقائي
4. الرابط: `https://math-competition-platform.vercel.app`

## 3️⃣ Heroku (مجاني محدود):
1. اذهب إلى: https://heroku.com
2. أنشئ تطبيق جديد
3. اربط GitHub
4. الرابط: `https://math-competition-platform.herokuapp.com`

## 4️⃣ Netlify (للواجهات):
1. اذهب إلى: https://netlify.com
2. اسحب وأفلت المجلد
3. نشر فوري

## 🎯 التوصية:
**Railway** هو الأفضل للمشاريع Django لأنه:
- ✅ يدعم Python/Django بشكل كامل
- ✅ قاعدة بيانات مجانية
- ✅ نشر تلقائي من GitHub
- ✅ مراقبة وسجلات
- ✅ دعم فني ممتاز
"""

        with open('ALTERNATIVE_SOLUTIONS.md', 'w', encoding='utf-8') as f:
            f.write(alternatives_content)
        
        print("✅ تم إنشاء ملف الحلول البديلة")
    
    def open_deployment_links(self):
        """فتح روابط النشر"""
        print("🌐 فتح روابط النشر...")
        
        links = [
            "https://github.com/new",
            "https://railway.app"
        ]
        
        for link in links:
            try:
                webbrowser.open(link)
                time.sleep(2)
            except:
                print(f"📋 افتح يدوياً: {link}")
    
    def run_deployment_process(self):
        """تشغيل عملية النشر"""
        print("🚂 بدء عملية النشر الدائم على Railway")
        print("="*50)
        
        # فحص المتطلبات
        if not self.check_requirements():
            return False
        
        # تحضير المشروع
        if not self.prepare_for_deployment():
            return False
        
        # إعداد Git
        if not self.setup_git_repo():
            return False
        
        # إنشاء الأدلة
        self.create_deployment_guide()
        self.create_alternative_solutions()
        
        print("\n" + "="*50)
        print("🎉 تم تحضير المشروع للنشر الدائم!")
        print("="*50)
        
        print("\n📋 الخطوات التالية:")
        print("1️⃣ ارفع المشروع على GitHub")
        print("2️⃣ انشر على Railway")
        print("3️⃣ احصل على رابط دائم")
        
        print("\n📄 اقرأ الملفات التالية للتفاصيل:")
        print("• RAILWAY_DEPLOYMENT_GUIDE.md - دليل مفصل")
        print("• ALTERNATIVE_SOLUTIONS.md - حلول بديلة")
        
        # سؤال عن فتح الروابط
        choice = input("\n❓ هل تريد فتح روابط النشر الآن؟ (y/n): ").lower().strip()
        
        if choice in ['y', 'yes', 'نعم', '1']:
            self.open_deployment_links()
            print("\n🌐 تم فتح الروابط في المتصفح")
        
        print("\n🎯 بعد النشر ستحصل على رابط دائم مثل:")
        print("https://math-competition-platform.railway.app/student/login/")
        print("🔑 رمز الدخول: ben25")
        
        return True

def main():
    """الدالة الرئيسية"""
    deployment = RailwayDeployment()
    deployment.run_deployment_process()

if __name__ == "__main__":
    main()
