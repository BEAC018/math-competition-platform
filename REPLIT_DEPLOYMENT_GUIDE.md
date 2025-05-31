# 🎮 دليل النشر على Replit

## 📁 الملفات المطلوبة للرفع:

### 📂 المجلدات الأساسية:
- `alhassan/` (إعدادات Django)
- `accounts/` (تطبيق الحسابات)
- `competitions/` (تطبيق المسابقات)
- `dashboard/` (لوحة التحكم)
- `templates/` (قوالب HTML)
- `static/` (ملفات CSS/JS)

### 📄 الملفات الأساسية:
- `manage.py`
- `requirements.txt`
- `db.sqlite3`

## 🚀 خطوات الرفع على Replit:

### 1. إنشاء Repl:
- اذهب إلى: https://replit.com
- انقر "Create Repl"
- اختر "Python"
- اسم المشروع: `math-competition-platform`

### 2. رفع الملفات:
- **طريقة 1:** اسحب وأفلت المجلدات من مجلد المشروع
- **طريقة 2:** انقر على أيقونة "Upload" في شريط الملفات
- **طريقة 3:** استخدم Git clone (متقدم)

### 3. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

### 4. إعداد قاعدة البيانات:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 5. إنشاء مستخدم إداري:
```bash
python manage.py createsuperuser
```

### 6. تشغيل الخادم:
```bash
python manage.py runserver 0.0.0.0:8000
```

## 🌐 الحصول على الرابط:

بعد تشغيل الخادم، ستحصل على رابط مثل:
```
https://math-competition-platform.your-username.repl.co
```

## 🎯 الرابط النهائي للتلاميذ:
```
https://math-competition-platform.your-username.repl.co/student/login/
```

## 🔑 معلومات الدخول:
- **رمز دخول التلاميذ:** ben25
- **رابط الأساتذة:** /competitions/student-analytics/

## ⚠️ ملاحظات مهمة:

1. **Keep Alive:** Replit قد يتوقف بعد عدم الاستخدام
2. **Always On:** يمكن ترقية الحساب لإبقاء التطبيق يعمل دائماً
3. **Database:** قاعدة البيانات ستُحفظ في Replit

## 🔧 إعدادات إضافية:

### ملف `.replit`:
```
run = "python manage.py runserver 0.0.0.0:8000"
language = "python3"

[nix]
channel = "stable-22_11"

[deployment]
run = ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
```

### متغيرات البيئة:
في Replit Secrets (قفل في الشريط الجانبي):
- `DEBUG`: False
- `SECRET_KEY`: مفتاح آمن جديد
