"""
URL configuration for alhassan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def home_view(request):
    """Home page with navigation"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>منصة المسابقات الرياضية</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; margin-bottom: 10px; }
            h2 { color: #34495e; margin-bottom: 30px; }
            .btn { display: inline-block; padding: 15px 30px; margin: 10px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; font-size: 16px; }
            .btn:hover { background: #2980b9; }
            .btn.admin { background: #e74c3c; }
            .btn.admin:hover { background: #c0392b; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧮 منصة المسابقات الرياضية</h1>
            <h2>Math Competition Platform</h2>
            <p>مرحباً بكم في منصة المسابقات الرياضية التفاعلية</p>

            <div style="margin: 30px 0;">
                <a href="/accounts/student/login/" class="btn">🎓 دخول الطلاب</a>
                <a href="/accounts/login/" class="btn">👨‍🏫 دخول المعلمين</a>
                <a href="/admin/" class="btn admin">⚙️ لوحة الإدارة</a>
            </div>

            <div style="margin: 20px 0;">
                <a href="/accounts/create-admin/" class="btn" style="background: #f39c12;">🔑 إنشاء حساب المدير</a>
            </div>

            <p style="color: #7f8c8d; margin-top: 30px;">
                رمز دخول الطلاب: <strong>ben25</strong>
            </p>
        </div>
    </body>
    </html>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('student/', include('competitions.urls')),
    path('dashboard/', include('dashboard.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
