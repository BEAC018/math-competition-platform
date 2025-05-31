# 🧮 منصة المسابقات الرياضية - Math Competition Platform

[![Django](https://img.shields.io/badge/Django-5.2.1-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## 📋 **نظرة عامة**

منصة تعليمية تفاعلية لإجراء مسابقات الحساب للطلاب من الصف الأول إلى التاسع. تتميز بواجهة عربية جميلة ونظام إدارة شامل للمعلمين.

## ✨ **الميزات الرئيسية**

### **🎯 للطلاب:**
- دخول سهل برمز `ben25`
- 9 مستويات صعوبة متدرجة
- أسئلة رياضية متنوعة (جمع، طرح، ضرب، قسمة)
- واجهة تفاعلية وجذابة
- نتائج فورية مع التقييم

### **👨‍🏫 للمعلمين:**
- إدارة شاملة للمشاركين
- إحصائيات مفصلة وتقارير
- تصدير البيانات إلى Excel/PDF
- تتبع تقدم الطلاب
- نظام تقييم متقدم

## 🚀 **المتطلبات الأساسية**

- [Python 3.8+](https://www.python.org/downloads/)
- [Django 5.2.1](https://www.djangoproject.com/)
- [Node.js 14+](https://nodejs.org/) (للملف التنفيذي)
- SQLite (مدمج مع Python)

## التثبيت

1. **تثبيت حزم Python المطلوبة**:

   ```bash
   # إنشاء بيئة افتراضية (اختياري ولكن موصى به)
   python -m venv venv

   # تفعيل البيئة الافتراضية
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate

   # تثبيت الحزم المطلوبة
   pip install -r requirements.txt
   ```

2. **تثبيت حزم Node.js المطلوبة**:

   ```bash
   npm install
   ```

3. **تعديل ملفات البدء (اختياري)**:

   إذا كنت تستخدم بيئة افتراضية أو تحتاج إلى تعديل إعدادات محددة، قم بتعديل:
   - `start_django.bat` (Windows)
   - `start_django.sh` (macOS/Linux)

## تشغيل التطبيق (وضع التطوير)

لتشغيل التطبيق في وضع التطوير، استخدم الأمر التالي:

```bash
npm start
```

هذا سيقوم بما يلي:
1. بدء تشغيل خادم Django على المنفذ 8000
2. بدء تشغيل تطبيق Electron الذي سيعرض واجهة الويب في نافذة سطح المكتب
3. تلقائيًا سيتم فتح التطبيق في وضع ملء الشاشة

## إنشاء تطبيق قابل للتوزيع

يمكنك إنشاء نسخة قابلة للتوزيع من التطبيق لنظام التشغيل المطلوب:

### Windows

```bash
npm run package-win
```

### macOS

```bash
npm run package-mac
```

### Linux

```bash
npm run package-linux
```

بعد الانتهاء، ستجد التطبيق القابل للتوزيع في مجلد `release-builds`.

## الميزات الرئيسية

- واجهة مستخدم كاملة الشاشة لتجربة غامرة
- تشغيل التطبيق كتطبيق سطح مكتب بدون الحاجة إلى متصفح
- دعم متعدد المنصات (Windows, macOS, Linux)
- واجهة مستخدم متجاوبة للحاسوب المحمول
- قفل مفتاح Escape لمنع الخروج من وضع ملء الشاشة عن طريق الخطأ

## ملاحظات هامة

- التطبيق يعمل محليًا ويتطلب تثبيت Python والحزم المطلوبة
- من الأفضل استخدام البيئة الافتراضية لتجنب تعارض الإصدارات