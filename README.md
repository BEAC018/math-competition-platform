# 🎯 منصة المسابقات الرياضية
## Math Competition Platform

[![Django](https://img.shields.io/badge/Django-5.2.1-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Railway](https://img.shields.io/badge/Deploy-Railway-blueviolet.svg)](https://railway.app)

## 🌟 نظرة عامة

منصة تفاعلية للمسابقات الرياضية مصممة خصيصاً للطلاب والمعلمين في المدارس العربية. تدعم المنصة النشر السحابي عبر Railway وGitHub.

## 🚀 النشر السريع

### نشر على Railway:
1. انقر على الزر أدناه للنشر المباشر:

   [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/django)

2. أو اتبع الخطوات اليدوية في قسم "النشر على Railway"

## ✨ المميزات الرئيسية

### 🎯 للطلاب:
- 🎮 واجهة سهلة الاستخدام
- 🔑 دخول سهل برمز `ben25`
- 📚 9 مستويات صعوبة متدرجة
- 🔢 أسئلة رياضية متنوعة (جمع، طرح، ضرب، قسمة)
- ⚡ نتائج فورية مع التقييم

### 👨‍🏫 للمعلمين:
- 📊 لوحة تحكم شاملة
- 📈 إحصائيات وتحليلات مفصلة
- 📋 تقارير قابلة للتصدير
- 👥 إدارة الطلاب والنتائج
- 🎯 تتبع التقدم والأداء

## 📋 المتطلبات

### للتطوير المحلي:
- Python 3.11+
- Django 5.2.1
- SQLite (مدمج مع Python)

### للنشر السحابي:
- حساب GitHub
- حساب Railway أو Heroku
- PostgreSQL (يتم توفيره تلقائياً)

## 🚀 التشغيل السريع

```bash
python start_local.py
```

## 🛠️ التثبيت اليدوي

### التطوير المحلي:
```bash
# استنساخ المشروع
git clone https://github.com/yourusername/math-competition-platform.git
cd math-competition-platform

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate

# تثبيت المتطلبات
pip install -r requirements.txt

# إعداد قاعدة البيانات
python manage.py migrate

# إنشاء حساب مدير
python manage.py createsuperuser

# تجميع الملفات الثابتة
python manage.py collectstatic

# تشغيل الخادم
python manage.py runserver 8090  # أو المنفذ المفضل لديك
```

## 🌐 النشر على Railway

### الطريقة الأولى: النشر المباشر
1. اذهب إلى [Railway](https://railway.app)
2. سجل دخولك باستخدام GitHub
3. انقر على "New Project"
4. اختر "Deploy from GitHub repo"
5. اختر هذا المستودع
6. Railway سيقوم بالنشر تلقائياً!

### الطريقة الثانية: النشر اليدوي
```bash
# تثبيت Railway CLI
npm install -g @railway/cli

# تسجيل الدخول
railway login

# ربط المشروع
railway link

# نشر المشروع
railway up
```

### إعداد متغيرات البيئة في Railway:
1. اذهب إلى لوحة تحكم Railway
2. اختر مشروعك
3. انقر على "Variables"
4. أضف المتغيرات التالية:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
STUDENT_ACCESS_CODE=ben25
ALLOWED_HOSTS=.railway.app
CSRF_TRUSTED_ORIGINS=https://yourapp.railway.app
```

## 🌐 النشر على Heroku

```bash
# تثبيت Heroku CLI
# ثم تسجيل الدخول
heroku login

# إنشاء تطبيق جديد
heroku create your-app-name

# إضافة PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# إعداد متغيرات البيئة
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set DEBUG=False
heroku config:set STUDENT_ACCESS_CODE=ben25

# نشر التطبيق
git push heroku main

# تشغيل الهجرات
heroku run python manage.py migrate

# إنشاء حساب مدير
heroku run python manage.py createsuperuser
```

## 🌐 الروابط

- **الصفحة الرئيسية**: http://localhost:8000
- **دخول التلاميذ**: http://localhost:8000/student/login/
- **دخول المعلمين**: http://localhost:8000/accounts/login/

## 🔑 معلومات الدخول

- **رمز دخول التلاميذ**: `ben25`
- **حساب المعلم**: يتم إنشاؤه عند أول تشغيل

## 📁 هيكل المشروع

```
📦 منصة المسابقات الرياضية/
├── 🏗️ alhassan/          # إعدادات Django الرئيسية
├── 👥 accounts/          # نظام المستخدمين والمعلمين
├── 🎯 competitions/      # نظام المسابقات والأسئلة
├── 📊 dashboard/         # لوحة التحكم والإحصائيات
├── 🎨 templates/         # قوالب HTML
├── 📁 static/           # ملفات CSS/JS/الصور
├── 📄 manage.py         # أداة إدارة Django
├── 📋 requirements.txt  # المتطلبات
└── 🗄️ db.sqlite3       # قاعدة البيانات
```

## 🎮 كيفية الاستخدام

### للطلاب:
1. انتقل إلى رابط دخول التلاميذ
2. أدخل اسمك
3. أدخل رمز الدخول: `ben25`
4. اختر مستواك الدراسي
5. ابدأ المسابقة!

### للمعلمين:
1. انتقل إلى رابط دخول المعلمين
2. سجل دخولك بحسابك
3. اطلع على الإحصائيات والنتائج
4. أدر المسابقات والطلاب

## 🔧 الإعدادات المتقدمة

### إنشاء حساب معلم جديد:
```bash
python manage.py createsuperuser
```

### إعادة تعيين قاعدة البيانات:
```bash
python manage.py flush
python manage.py migrate
```

## 📊 المميزات التقنية

- **Framework**: Django 5.2
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js للرسوم البيانية
- **Responsive**: Bootstrap للتصميم المتجاوب

## 🎯 أنواع الأسئلة المدعومة

- ➕ الجمع (مستويات متعددة)
- ➖ الطرح (مستويات متعددة)
- ✖️ الضرب (جداول الضرب)
- ➗ القسمة (مع وبدون باقي)
- 🔢 العمليات المختلطة
- 🧮 المسائل الكلامية

## 📈 الإحصائيات والتحليلات

- 📊 نتائج الطلاب حسب المستوى
- 📈 تقدم الطلاب عبر الزمن
- 🎯 تحليل نقاط القوة والضعف
- 📋 تقارير مفصلة قابلة للتصدير

## 🔧 استكشاف الأخطاء وإصلاحها

### مشاكل شائعة:

#### خطأ في قاعدة البيانات:
```bash
# إعادة تعيين قاعدة البيانات
python manage.py flush
python manage.py migrate
```

#### مشاكل الملفات الثابتة:
```bash
# إعادة تجميع الملفات الثابتة
python manage.py collectstatic --clear --noinput
```

#### مشاكل متغيرات البيئة:
- تأكد من إعداد جميع المتغيرات المطلوبة
- راجع ملف `.env.example` للمرجع

### سجلات الأخطاء:
```bash
# عرض سجلات Railway
railway logs

# عرض سجلات Heroku
heroku logs --tail
```

## 🔐 الأمان

### للنشر الإنتاجي:
1. **لا تستخدم** `DEBUG=True` في الإنتاج
2. استخدم `SECRET_KEY` قوي ومختلف
3. قم بتحديد `ALLOWED_HOSTS` بدقة
4. فعّل HTTPS دائماً
5. استخدم متغيرات البيئة للمعلومات الحساسة

### إنشاء SECRET_KEY جديد:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## 📚 الوثائق الإضافية

- [وثائق Django](https://docs.djangoproject.com/)
- [وثائق Railway](https://docs.railway.app/)
- [وثائق Heroku](https://devcenter.heroku.com/)

## 🤝 المساهمة

1. Fork المشروع
2. إنشاء فرع للميزة الجديدة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى الفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 📞 الدعم

إذا واجهت أي مشاكل أو لديك أسئلة:
- افتح [Issue جديد](https://github.com/yourusername/math-competition-platform/issues)
- راسلنا على البريد الإلكتروني

---

**🎯 استمتعوا بالتعلم والمنافسة الشريفة! 🚀**

## 📊 إحصائيات المشروع

![GitHub stars](https://img.shields.io/github/stars/yourusername/math-competition-platform)
![GitHub forks](https://img.shields.io/github/forks/yourusername/math-competition-platform)
![GitHub issues](https://img.shields.io/github/issues/yourusername/math-competition-platform)
![GitHub license](https://img.shields.io/github/license/yourusername/math-competition-platform)