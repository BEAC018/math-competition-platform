"""
إعدادات الإنتاج لمنصة المسابقات الرياضية
Production settings for Math Competition Platform
"""

from .settings import *
import os

# إعدادات الأمان للإنتاج
DEBUG = False
ALLOWED_HOSTS = [
    '.replit.app',
    '.replit.dev', 
    '.repl.co',
    '.railway.app',
    '.herokuapp.com',
    '.render.com',
    '.vercel.app',
    '.netlify.app',
    '.ngrok.io',
    '.ngrok-free.app',
    '.ngrok.app',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '*'  # للتطوير فقط - احذف في الإنتاج الحقيقي
]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://*.replit.app',
    'https://*.replit.dev',
    'https://*.repl.co',
    'https://*.railway.app',
    'https://*.herokuapp.com',
    'https://*.render.com',
    'https://*.vercel.app',
    'https://*.netlify.app',
    'https://*.ngrok.io',
    'https://*.ngrok-free.app',
    'https://*.ngrok.app',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# إعدادات قاعدة البيانات للإنتاج
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
    # إعدادات إضافية لـ PostgreSQL
    DATABASES['default']['CONN_MAX_AGE'] = 600
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'require',
    }
else:
    # SQLite للتطوير والاختبار
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# إعدادات الأمان المحسنة
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# إعدادات الملفات الثابتة للإنتاج
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# WhiteNoise للملفات الثابتة
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# إعدادات التسجيل للإنتاج
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# إعدادات الجلسات
SESSION_COOKIE_SECURE = False  # True في HTTPS فقط
CSRF_COOKIE_SECURE = False     # True في HTTPS فقط
SESSION_COOKIE_AGE = 3600      # ساعة واحدة
