#!/bin/bash

# تحديد متغيرات البيئة
export DJANGO_SETTINGS_MODULE=alhassan.settings
export PYTHONPATH=.

# تطبيق migrations
python manage.py migrate --noinput

# جمع الملفات الثابتة
python manage.py collectstatic --noinput --clear

# تشغيل الخادم
if [ "$PORT" ]; then
    gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
else
    gunicorn alhassan.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
fi
