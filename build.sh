#!/usr/bin/env bash
# Build script for Render deployment
# سكريبت البناء للنشر على Render

set -o errexit  # Exit on error

echo "🚀 بدء عملية البناء..."
echo "Starting build process..."

echo "📦 تثبيت المتطلبات..."
echo "Installing requirements..."
pip install -r requirements.txt

echo "📁 إنشاء مجلدات الملفات الثابتة..."
echo "Creating static directories..."
mkdir -p staticfiles
mkdir -p static

echo "📁 جمع الملفات الثابتة..."
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || echo "Static files collection failed, continuing..."

echo "📊 تطبيق هجرات قاعدة البيانات..."
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "✅ اكتمل البناء بنجاح!"
echo "Build completed successfully!"
