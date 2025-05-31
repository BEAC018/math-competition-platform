"""
إعدادات Django محدثة لـ Railway
Updated Django settings for Railway deployment
"""

# إعدادات قاعدة البيانات لـ Railway
RAILWAY_DATABASE_SETTINGS = """
import os
import dj_database_url

# إعدادات قاعدة البيانات
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# إعدادات الإنتاج
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',
    '.up.railway.app',
    '.onrender.com',
    '.herokuapp.com',
    '.vercel.app'
]

# إعدادات الملفات الثابتة
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# إعدادات الأمان
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-change-in-production')

# إعدادات CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# إعدادات الجلسات
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# إعدادات المنطقة الزمنية
USE_TZ = True
TIME_ZONE = 'UTC'
"""

# متطلبات إضافية لـ Railway
ADDITIONAL_REQUIREMENTS = """
dj-database-url==2.1.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
gunicorn==21.2.0
"""

# Procfile محدث
UPDATED_PROCFILE = """web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn alhassan.wsgi:application --bind 0.0.0.0:$PORT"""

# متغيرات البيئة المطلوبة
REQUIRED_ENV_VARS = {
    'DEBUG': 'False',
    'DJANGO_SETTINGS_MODULE': 'alhassan.settings',
    'SECRET_KEY': 'django-insecure-math-platform-railway-2024-xyz123',
    'ALLOWED_HOSTS': '.railway.app,.up.railway.app,localhost,127.0.0.1',
    'PORT': '8000',
    'PYTHONPATH': '/app',
    'STATIC_URL': '/static/',
    'STATIC_ROOT': 'staticfiles'
}

def create_fixed_files():
    """إنشاء ملفات محدثة للإصلاح"""
    
    # إنشاء requirements.txt محدث
    with open('requirements_railway.txt', 'w') as f:
        f.write("""Django==4.2.7
dj-database-url==2.1.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
gunicorn==21.2.0
django-cors-headers==4.3.1
Pillow==10.1.0
""")
    
    # إنشاء Procfile محدث
    with open('Procfile_railway', 'w') as f:
        f.write(UPDATED_PROCFILE)
    
    # إنشاء ملف إعدادات محدث
    with open('settings_railway.py', 'w') as f:
        f.write(f"""
# إعدادات Django لـ Railway
import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

{RAILWAY_DATABASE_SETTINGS}

# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'competitions',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alhassan.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = 'alhassan.wsgi.application'

# إعدادات اللغة
LANGUAGE_CODE = 'ar'
USE_I18N = True
USE_L10N = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# إعدادات Whitenoise للملفات الثابتة
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
""")
    
    print("✅ تم إنشاء ملفات الإصلاح:")
    print("📄 requirements_railway.txt")
    print("📄 Procfile_railway") 
    print("📄 settings_railway.py")

if __name__ == "__main__":
    create_fixed_files()
