from django.http import HttpResponse


def handler500(request):
    """معالج خطأ 500 - يعيد توجيه للنظام الطارئ"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>إعادة توجيه - منصة المسابقات الرياضية</title>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
                margin: 0;
            }
            .card {
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }
            .icon {
                font-size: 4em;
                margin-bottom: 20px;
            }
            .title {
                color: #2c3e50;
                font-size: 2em;
                margin-bottom: 15px;
            }
            .message {
                color: #7f8c8d;
                font-size: 1.1em;
                margin-bottom: 30px;
                line-height: 1.6;
            }
            .btn {
                padding: 15px 30px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: bold;
                margin: 10px;
                display: inline-block;
                transition: all 0.3s;
            }
            .btn-primary { background: #3498db; color: white; }
            .btn-success { background: #27ae60; color: white; }
            .btn-warning { background: #f39c12; color: white; }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .countdown {
                color: #e74c3c;
                font-weight: bold;
                font-size: 1.2em;
            }
        </style>
        <script>
            let countdown = 5;
            function updateCountdown() {
                document.getElementById('countdown').textContent = countdown;
                countdown--;
                if (countdown < 0) {
                    window.location.href = '/emergency/';
                }
            }
            setInterval(updateCountdown, 1000);
            updateCountdown();
        </script>
    </head>
    <body>
        <div class="card">
            <div class="icon">🚨</div>
            <h1 class="title">تم اكتشاف مشكلة تقنية</h1>
            <p class="message">
                سيتم إعادة توجيهك للنظام الطارئ الذي يعمل بدون قاعدة البيانات.
                هذا النظام يوفر جميع الوظائف الأساسية للمنصة.
            </p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p class="countdown">إعادة التوجيه خلال <span id="countdown">5</span> ثوان...</p>
            </div>
            
            <div style="margin: 30px 0;">
                <a href="/emergency/" class="btn btn-primary">🚨 النظام الطارئ</a>
                <a href="/emergency/student/" class="btn btn-success">🎓 دخول الطلاب</a>
                <a href="/" class="btn btn-warning">🏠 الصفحة الرئيسية</a>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ecf0f1;">
                <p style="color: #95a5a6; font-size: 0.9em;">
                    النظام الطارئ يوفر جميع وظائف المسابقات بدون الحاجة لقاعدة البيانات
                </p>
            </div>
        </div>
    </body>
    </html>
    """, status=500)


def handler404(request, exception):
    """معالج خطأ 404"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>الصفحة غير موجودة - منصة المسابقات الرياضية</title>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
                margin: 0;
            }
            .card {
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }
            .btn {
                padding: 15px 30px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: bold;
                margin: 10px;
                display: inline-block;
                background: #3498db;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div style="font-size: 4em; margin-bottom: 20px;">🔍</div>
            <h1 style="color: #2c3e50; margin-bottom: 15px;">الصفحة غير موجودة</h1>
            <p style="color: #7f8c8d; margin-bottom: 30px;">
                الصفحة التي تبحث عنها غير موجودة أو تم نقلها.
            </p>
            <div>
                <a href="/" class="btn">🏠 الصفحة الرئيسية</a>
                <a href="/emergency/student/" class="btn">🎓 دخول الطلاب</a>
                <a href="/emergency/" class="btn">🚨 النظام الطارئ</a>
            </div>
        </div>
    </body>
    </html>
    """, status=404)
