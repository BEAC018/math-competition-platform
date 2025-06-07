#!/usr/bin/env bash
# Build script without collectstatic
# سكريبت بناء بدون جمع الملفات الثابتة

set -o errexit

echo "🚀 بدء البناء بدون collectstatic..."
echo "Starting build without collectstatic..."

echo "📦 تثبيت المتطلبات الأساسية..."
echo "Installing basic requirements..."
pip install Django==5.2.1 gunicorn==21.2.0 whitenoise==6.6.0

echo "📊 تطبيق هجرات قاعدة البيانات..."
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "✅ البناء مكتمل بنجاح!"
echo "Build completed successfully!"
