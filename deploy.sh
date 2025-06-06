#!/bin/bash

# 🚀 سكريبت النشر التلقائي لمنصة المسابقات الرياضية
# Automatic deployment script for Math Competition Platform

echo "🚀 بدء عملية النشر..."
echo "Starting deployment process..."

# تحديد متغيرات البيئة
export DJANGO_SETTINGS_MODULE=alhassan.production_settings
export PYTHONPATH=.

echo "📊 تطبيق هجرات قاعدة البيانات..."
echo "Applying database migrations..."
python manage.py migrate --noinput

if [ $? -eq 0 ]; then
    echo "✅ تم تطبيق الهجرات بنجاح"
    echo "✅ Migrations applied successfully"
else
    echo "❌ فشل في تطبيق الهجرات"
    echo "❌ Failed to apply migrations"
    exit 1
fi

echo "📁 جمع الملفات الثابتة..."
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

if [ $? -eq 0 ]; then
    echo "✅ تم جمع الملفات الثابتة بنجاح"
    echo "✅ Static files collected successfully"
else
    echo "❌ فشل في جمع الملفات الثابتة"
    echo "❌ Failed to collect static files"
    exit 1
fi

echo "🔧 فحص النظام..."
echo "Running system checks..."
python manage.py check --deploy

if [ $? -eq 0 ]; then
    echo "✅ فحص النظام مكتمل بنجاح"
    echo "✅ System check completed successfully"
else
    echo "⚠️ تحذيرات في فحص النظام"
    echo "⚠️ System check warnings detected"
fi

echo "🌐 بدء تشغيل الخادم..."
echo "Starting server..."

# تشغيل الخادم
if [ "$PORT" ]; then
    echo "🚀 تشغيل على المنفذ: $PORT"
    echo "🚀 Running on port: $PORT"
    gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120 --access-logfile - --error-logfile -
else
    echo "🚀 تشغيل على المنفذ الافتراضي: 8000"
    echo "🚀 Running on default port: 8000"
    gunicorn alhassan.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120 --access-logfile - --error-logfile -
fi
