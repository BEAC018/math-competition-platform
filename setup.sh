#!/bin/bash

echo "🚀 بدء إعداد منصة المسابقات الرياضية..."

# تثبيت المتطلبات
echo "📦 تثبيت المتطلبات..."
pip install -r requirements.txt

# إنشاء migrations
echo "📊 إنشاء migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations competitions
python manage.py makemigrations dashboard

# تطبيق migrations
echo "🔄 تطبيق migrations..."
python manage.py migrate

# إنشاء مدير النظام
echo "👤 إنشاء مدير النظام..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@mathcompetition.com',
        password='admin123456',
        first_name='مدير',
        last_name='النظام'
    )
    print("✅ تم إنشاء المدير بنجاح")
else:
    print("✅ المدير موجود مسبقاً")
EOF

# جمع الملفات الثابتة
echo "📁 جمع الملفات الثابتة..."
python manage.py collectstatic --noinput

echo "🎉 تم إعداد النظام بنجاح!"
echo "📋 بيانات الدخول:"
echo "   اسم المستخدم: admin"
echo "   كلمة المرور: admin123456"
echo "   رمز دخول الطلاب: ben25"
