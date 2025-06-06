from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import connection, OperationalError
from django.shortcuts import redirect
import os


def setup_system(request):
    """إعداد النظام بالكامل"""
    try:
        # تشغيل migrations
        call_command('makemigrations', verbosity=0, interactive=False)
        call_command('migrate', verbosity=0, interactive=False)
        
        # إنشاء مدير إذا لم يكن موجود
        admin_created = False
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@mathcompetition.com',
                password='admin123456',
                first_name='مدير',
                last_name='النظام'
            )
            admin_created = True
        
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>تم إعداد النظام - منصة المسابقات الرياضية</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}
                .success-card {{
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    max-width: 600px;
                    width: 100%;
                    text-align: center;
                }}
                .success-icon {{
                    font-size: 4em;
                    margin-bottom: 20px;
                    color: #27ae60;
                }}
                .success-title {{
                    color: #2c3e50;
                    font-size: 2em;
                    margin-bottom: 15px;
                }}
                .success-message {{
                    color: #7f8c8d;
                    font-size: 1.1em;
                    margin-bottom: 30px;
                    line-height: 1.6;
                }}
                .admin-info {{
                    background: #d4edda;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    border: 1px solid #c3e6cb;
                }}
                .btn {{
                    padding: 12px 24px;
                    border-radius: 10px;
                    text-decoration: none;
                    font-weight: bold;
                    margin: 5px;
                    display: inline-block;
                    transition: all 0.3s;
                }}
                .btn-primary {{ background: #3498db; color: white; }}
                .btn-success {{ background: #27ae60; color: white; }}
                .btn-warning {{ background: #f39c12; color: white; }}
                .btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }}
            </style>
        </head>
        <body>
            <div class="success-card">
                <div class="success-icon">🎉</div>
                <h1 class="success-title">تم إعداد النظام بنجاح!</h1>
                <p class="success-message">
                    تم إنشاء قاعدة البيانات وإعداد جميع الجداول المطلوبة.
                    النظام جاهز الآن للاستخدام!
                </p>
                
                {'<div class="admin-info"><h3 style="color: #155724;">🔑 تم إنشاء حساب المدير</h3><p><strong>اسم المستخدم:</strong> admin</p><p><strong>كلمة المرور:</strong> admin123456</p><p style="color: #856404; font-size: 0.9em;">احفظ هذه البيانات في مكان آمن</p></div>' if admin_created else '<div class="admin-info"><h3 style="color: #155724;">✅ حساب المدير موجود مسبقاً</h3></div>'}
                
                <div style="margin: 30px 0;">
                    <a href="/" class="btn btn-primary">🏠 الصفحة الرئيسية</a>
                    <a href="/accounts/student/login/" class="btn btn-success">🎓 دخول الطلاب</a>
                    <a href="/accounts/login/" class="btn btn-warning">👨‍🏫 دخول المعلمين</a>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ecf0f1;">
                    <p style="color: #95a5a6; font-size: 0.9em;">
                        جميع الصفحات تعمل الآن بشكل طبيعي
                    </p>
                </div>
            </div>
        </body>
        </html>
        """)
        
    except Exception as e:
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>خطأ في الإعداد - منصة المسابقات الرياضية</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}
                .error-card {{
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    max-width: 600px;
                    width: 100%;
                    text-align: center;
                }}
                .btn {{
                    padding: 12px 24px;
                    border-radius: 10px;
                    text-decoration: none;
                    font-weight: bold;
                    margin: 5px;
                    display: inline-block;
                    background: #3498db;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="error-card">
                <h1 style="color: #e74c3c; margin-bottom: 20px;">❌ خطأ في الإعداد</h1>
                <p style="color: #7f8c8d; margin-bottom: 20px;">حدث خطأ أثناء إعداد النظام:</p>
                <p style="color: #e74c3c; margin-bottom: 30px;">{str(e)}</p>
                <a href="/setup/" class="btn">🔄 إعادة المحاولة</a>
                <a href="/" class="btn">🏠 الصفحة الرئيسية</a>
            </div>
        </body>
        </html>
        """, status=500)


def check_system_status(request):
    """فحص حالة النظام"""
    try:
        # فحص قاعدة البيانات
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
        
        # فحص وجود المدير
        admin_exists = User.objects.filter(is_superuser=True).exists()
        
        status = {
            'database_ready': len(tables) >= 5,
            'admin_exists': admin_exists,
            'tables_count': len(tables)
        }
        
        return HttpResponse(f"""
        <div style="padding: 20px; font-family: Arial;">
            <h2>حالة النظام</h2>
            <p>قاعدة البيانات: {'✅ جاهزة' if status['database_ready'] else '❌ غير جاهزة'}</p>
            <p>المدير: {'✅ موجود' if status['admin_exists'] else '❌ غير موجود'}</p>
            <p>عدد الجداول: {status['tables_count']}</p>
            <a href="/setup/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">إعداد النظام</a>
        </div>
        """)
        
    except Exception as e:
        return HttpResponse(f"""
        <div style="padding: 20px; font-family: Arial;">
            <h2>خطأ في فحص النظام</h2>
            <p style="color: red;">{str(e)}</p>
            <a href="/setup/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">إعداد النظام</a>
        </div>
        """)
