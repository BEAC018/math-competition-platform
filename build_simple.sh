#!/usr/bin/env bash
# Simple build script for Render - No collectstatic
# سكريبت بناء مبسط بدون collectstatic

set -o errexit

echo "🚀 بدء البناء المبسط..."
echo "Starting simple build..."

echo "📦 تثبيت Django والمتطلبات الأساسية..."
echo "Installing Django and basic requirements..."
pip install Django==5.2.1 gunicorn==21.2.0 whitenoise==6.6.0

echo "📊 تطبيق هجرات قاعدة البيانات..."
echo "Applying database migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

echo "✅ البناء المبسط مكتمل!"
echo "Simple build completed!"
