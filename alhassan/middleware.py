from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import connection, OperationalError
import os


class DatabaseSetupMiddleware:
    """Middleware لإعداد قاعدة البيانات تلقائياً"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.setup_attempted = False

    def __call__(self, request):
        # محاولة إعداد قاعدة البيانات إذا لم تكن جاهزة
        if not self.setup_attempted:
            try:
                # التحقق من وجود جداول قاعدة البيانات
                with connection.cursor() as cursor:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                
                # إذا لم توجد جداول، قم بإعداد قاعدة البيانات
                if len(tables) < 5:  # عدد قليل من الجداول يعني أن قاعدة البيانات غير مكتملة
                    self.setup_database()
                
                self.setup_attempted = True
                
            except OperationalError:
                # قاعدة البيانات غير موجودة، قم بإنشائها
                self.setup_database()
                self.setup_attempted = True
            except Exception:
                # في حالة أي خطأ آخر، تجاهل واستمر
                self.setup_attempted = True

        response = self.get_response(request)
        return response

    def setup_database(self):
        """إعداد قاعدة البيانات"""
        try:
            # تشغيل migrations
            call_command('makemigrations', verbosity=0, interactive=False)
            call_command('migrate', verbosity=0, interactive=False)
            
            # إنشاء مدير إذا لم يكن موجود
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@mathcompetition.com',
                    password='admin123456',
                    first_name='مدير',
                    last_name='النظام'
                )
        except Exception:
            # في حالة فشل الإعداد، تجاهل واستمر
            pass


class ErrorHandlingMiddleware:
    """Middleware لمعالجة الأخطاء وعرض صفحات بديلة"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            # في حالة حدوث خطأ، عرض صفحة خطأ مخصصة
            return self.handle_error(request, e)

    def handle_error(self, request, error):
        """معالجة الأخطاء وعرض صفحة بديلة"""
        error_message = str(error)
        
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>خطأ مؤقت - منصة المسابقات الرياضية</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                .error-icon {{
                    font-size: 4em;
                    margin-bottom: 20px;
                }}
                .error-title {{
                    color: #2c3e50;
                    font-size: 2em;
                    margin-bottom: 15px;
                }}
                .error-message {{
                    color: #7f8c8d;
                    font-size: 1.1em;
                    margin-bottom: 30px;
                    line-height: 1.6;
                }}
                .error-actions {{
                    display: flex;
                    gap: 15px;
                    justify-content: center;
                    flex-wrap: wrap;
                }}
                .btn {{
                    padding: 12px 24px;
                    border-radius: 10px;
                    text-decoration: none;
                    font-weight: bold;
                    transition: all 0.3s;
                }}
                .btn-primary {{
                    background: #3498db;
                    color: white;
                }}
                .btn-secondary {{
                    background: #95a5a6;
                    color: white;
                }}
                .btn-success {{
                    background: #27ae60;
                    color: white;
                }}
                .btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }}
                .setup-info {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    border-left: 4px solid #3498db;
                }}
            </style>
        </head>
        <body>
            <div class="error-card">
                <div class="error-icon">🔧</div>
                <h1 class="error-title">جاري إعداد النظام</h1>
                <p class="error-message">
                    النظام يقوم بإعداد قاعدة البيانات تلقائياً. 
                    يرجى الانتظار قليلاً ثم إعادة تحديث الصفحة.
                </p>
                
                <div class="setup-info">
                    <h3>ما يحدث الآن:</h3>
                    <ul style="text-align: right; margin: 10px 0;">
                        <li>إنشاء جداول قاعدة البيانات</li>
                        <li>إعداد حساب المدير</li>
                        <li>تهيئة النظام للاستخدام</li>
                    </ul>
                </div>
                
                <div class="error-actions">
                    <a href="javascript:location.reload()" class="btn btn-primary">🔄 إعادة تحديث</a>
                    <a href="/" class="btn btn-secondary">🏠 الصفحة الرئيسية</a>
                    <a href="/accounts/create-admin/" class="btn btn-success">🔑 إنشاء المدير</a>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ecf0f1;">
                    <p style="color: #95a5a6; font-size: 0.9em;">
                        إذا استمرت المشكلة، يرجى المحاولة مرة أخرى خلال دقيقة
                    </p>
                </div>
            </div>
            
            <script>
                // إعادة تحديث تلقائي بعد 10 ثوان
                setTimeout(function() {{
                    location.reload();
                }}, 10000);
            </script>
        </body>
        </html>
        """, status=500)
