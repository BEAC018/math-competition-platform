#!/bin/bash
echo "🚀 بدء تشغيل منصة المسابقات الرياضية..."

# تثبيت المتطلبات
echo "📦 تثبيت المتطلبات..."
pip install -r requirements.txt

# إعداد قاعدة البيانات
echo "🗄️ إعداد قاعدة البيانات..."
python manage.py migrate

# جمع الملفات الثابتة
echo "📁 جمع الملفات الثابتة..."
python manage.py collectstatic --noinput

# تشغيل الخادم
echo "🌐 تشغيل الخادم..."
echo "📍 رابط المنصة: https://$REPL_SLUG.$REPL_OWNER.repl.co"
echo "👥 رابط التلاميذ: https://$REPL_SLUG.$REPL_OWNER.repl.co/student/login/"
echo "🔑 رمز الدخول: ben25"

python manage.py runserver 0.0.0.0:8000