from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import connection, OperationalError
from django.middleware.csrf import get_token
import traceback


def emergency_setup(request):
    """إعداد طارئ للنظام - يعمل في جميع الحالات"""
    try:
        # محاولة إعداد قاعدة البيانات
        call_command('migrate', verbosity=0, interactive=False)
        
        # إنشاء مدير
        admin_created = False
        try:
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@mathcompetition.com',
                    password='admin123456'
                )
                admin_created = True
        except:
            pass
        
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>تم الإعداد - منصة المسابقات الرياضية</title>
            <style>
                body {{ font-family: Arial; background: #27ae60; color: white; text-align: center; padding: 50px; }}
                .card {{ background: white; color: #2c3e50; padding: 40px; border-radius: 15px; max-width: 600px; margin: 0 auto; }}
                .btn {{ background: #3498db; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; margin: 10px; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🎉 تم إعداد النظام بنجاح!</h1>
                {'<p><strong>تم إنشاء المدير:</strong> admin / admin123456</p>' if admin_created else '<p>المدير موجود مسبقاً</p>'}
                <div style="margin: 30px 0;">
                    <a href="/" class="btn">🏠 الصفحة الرئيسية</a>
                    <a href="/accounts/student/login/" class="btn">🎓 دخول الطلاب</a>
                    <a href="/accounts/login/" class="btn">👨‍🏫 دخول المعلمين</a>
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
            <title>خطأ - منصة المسابقات الرياضية</title>
            <style>
                body {{ font-family: Arial; background: #e74c3c; color: white; text-align: center; padding: 50px; }}
                .card {{ background: white; color: #2c3e50; padding: 40px; border-radius: 15px; max-width: 600px; margin: 0 auto; }}
                .btn {{ background: #3498db; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; margin: 10px; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>❌ خطأ في الإعداد</h1>
                <p>حدث خطأ: {str(e)}</p>
                <div style="margin: 30px 0;">
                    <a href="/emergency/" class="btn">🔄 إعادة المحاولة</a>
                    <a href="/" class="btn">🏠 الصفحة الرئيسية</a>
                </div>
            </div>
        </body>
        </html>
        """)


def emergency_student_login(request):
    """صفحة دخول طلاب طارئة - تعمل بدون قاعدة بيانات"""
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        access_code = request.POST.get('access_code')
        grade_level = request.POST.get('grade_level')
        difficulty_level = request.POST.get('difficulty_level')
        
        if access_code == 'ben25':
            # حفظ في الجلسة مباشرة
            request.session['student_name'] = student_name
            request.session['grade_level'] = grade_level
            request.session['difficulty_level'] = difficulty_level
            return redirect('/emergency/competition/')
        else:
            error_msg = "رمز الدخول غير صحيح. الرمز الصحيح: ben25"
    else:
        error_msg = ""
    
    csrf_token = get_token(request)
    
    return HttpResponse(f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>دخول الطلاب - منصة المسابقات الرياضية</title>
        <style>
            body {{ font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
            .card {{ background: white; border-radius: 20px; padding: 40px; max-width: 500px; width: 100%; }}
            .form-group {{ margin-bottom: 20px; }}
            .form-group label {{ display: block; margin-bottom: 8px; color: #2c3e50; font-weight: bold; }}
            .form-group input, .form-group select {{ width: 100%; padding: 15px; border: 2px solid #ecf0f1; border-radius: 10px; font-size: 16px; }}
            .btn {{ width: 100%; padding: 15px; background: #27ae60; color: white; border: none; border-radius: 10px; font-size: 18px; cursor: pointer; }}
            .error {{ background: #f8d7da; color: #721c24; padding: 15px; border-radius: 10px; margin-bottom: 20px; }}
            .nav-links {{ text-align: center; margin-top: 30px; }}
            .nav-links a {{ color: #3498db; text-decoration: none; margin: 0 15px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #2c3e50;">🎓 دخول الطلاب</h1>
                <h2 style="color: #7f8c8d; font-weight: normal;">مرحباً بك في منصة المسابقات الرياضية</h2>
            </div>
            
            {'<div class="error">' + error_msg + '</div>' if error_msg else ''}
            
            <form method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="form-group">
                    <label for="student_name">اسم الطالب:</label>
                    <input type="text" id="student_name" name="student_name" required placeholder="أدخل اسمك الكامل">
                </div>
                
                <div class="form-group">
                    <label for="access_code">رمز الدخول:</label>
                    <input type="text" id="access_code" name="access_code" required placeholder="أدخل رمز الدخول">
                    <small style="color: #7f8c8d;">رمز الدخول: ben25</small>
                </div>
                
                <div class="form-group">
                    <label for="grade_level">المستوى الدراسي:</label>
                    <select id="grade_level" name="grade_level" required>
                        <option value="">اختر المستوى</option>
                        <option value="الصف الأول">الصف الأول</option>
                        <option value="الصف الثاني">الصف الثاني</option>
                        <option value="الصف الثالث">الصف الثالث</option>
                        <option value="الصف الرابع">الصف الرابع</option>
                        <option value="الصف الخامس">الصف الخامس</option>
                        <option value="الصف السادس">الصف السادس</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="difficulty_level">مستوى الصعوبة:</label>
                    <select id="difficulty_level" name="difficulty_level" required>
                        <option value="">اختر مستوى الصعوبة</option>
                        <option value="easy">سهل 😊 - أرقام صغيرة وعمليات بسيطة</option>
                        <option value="medium">متوسط 🤔 - أرقام متوسطة وعمليات متنوعة</option>
                        <option value="hard">صعب 🔥 - أرقام كبيرة وعمليات معقدة</option>
                    </select>
                </div>
                
                <button type="submit" class="btn">🚀 ابدأ المسابقة</button>
            </form>
            
            <div class="nav-links">
                <a href="/">🏠 الصفحة الرئيسية</a>
                <a href="/emergency/">🔧 إعداد النظام</a>
            </div>
        </div>
    </body>
    </html>
    """)


def emergency_competition(request):
    """مسابقة طارئة - تعمل بدون قاعدة بيانات"""
    if 'student_name' not in request.session:
        return redirect('/emergency/student/')
    
    import random
    
    # توليد سؤال عشوائي
    difficulty = request.session.get('difficulty_level', 'medium')
    
    if difficulty == 'easy':
        a, b = random.randint(1, 20), random.randint(1, 20)
    elif difficulty == 'hard':
        a, b = random.randint(50, 200), random.randint(50, 200)
    else:
        a, b = random.randint(10, 100), random.randint(10, 100)
    
    operations = ['+', '-', '×', '÷']
    op = random.choice(operations)
    
    if op == '+':
        answer = a + b
        question = f"{a} + {b}"
    elif op == '-':
        if a < b:
            a, b = b, a
        answer = a - b
        question = f"{a} - {b}"
    elif op == '×':
        if difficulty == 'easy':
            a, b = random.randint(1, 10), random.randint(1, 10)
        answer = a * b
        question = f"{a} × {b}"
    else:  # ÷
        if difficulty == 'easy':
            b = random.randint(2, 10)
            answer = random.randint(1, 10)
        else:
            b = random.randint(2, 20)
            answer = random.randint(1, 20)
        a = b * answer
        question = f"{a} ÷ {b}"
    
    csrf_token = get_token(request)
    student_name = request.session.get('student_name')
    
    return HttpResponse(f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>المسابقة - منصة المسابقات الرياضية</title>
        <style>
            body {{ font-family: Arial; background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
            .card {{ background: white; border-radius: 20px; padding: 40px; max-width: 600px; width: 100%; text-align: center; }}
            .question {{ font-size: 3em; color: #2c3e50; margin: 30px 0; background: #f8f9fa; padding: 30px; border-radius: 15px; }}
            .form-group {{ margin: 30px 0; }}
            .form-group input {{ font-size: 1.5em; padding: 15px; border: 2px solid #ecf0f1; border-radius: 10px; text-align: center; width: 200px; }}
            .btn {{ padding: 15px 30px; background: #27ae60; color: white; border: none; border-radius: 10px; font-size: 18px; cursor: pointer; }}
            .student-info {{ color: #7f8c8d; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1 style="color: #2c3e50;">🧮 مسابقة الرياضيات</h1>
            <div class="student-info">الطالب: {student_name}</div>
            
            <div class="question">{question} = ؟</div>
            
            <form method="post" action="/emergency/check/">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <input type="hidden" name="question" value="{question}">
                <input type="hidden" name="answer" value="{answer}">
                
                <div class="form-group">
                    <label style="font-size: 1.2em; margin-bottom: 10px; display: block;">أدخل إجابتك:</label>
                    <input type="number" name="student_answer" required placeholder="الإجابة" autofocus>
                </div>
                
                <button type="submit" class="btn">✅ إرسال الإجابة</button>
            </form>
            
            <div style="margin-top: 30px;">
                <a href="/emergency/student/" style="color: #3498db; text-decoration: none;">🔙 العودة لدخول الطلاب</a>
            </div>
        </div>
    </body>
    </html>
    """)


def emergency_check_answer(request):
    """فحص الإجابة"""
    if request.method == 'POST':
        question = request.POST.get('question')
        correct_answer = int(request.POST.get('answer'))
        student_answer = int(request.POST.get('student_answer', 0))
        
        is_correct = student_answer == correct_answer
        
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>النتيجة - منصة المسابقات الرياضية</title>
            <style>
                body {{ font-family: Arial; background: {'linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)' if is_correct else 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)'}; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
                .card {{ background: white; border-radius: 20px; padding: 40px; max-width: 600px; width: 100%; text-align: center; }}
                .result {{ font-size: 4em; margin: 20px 0; }}
                .btn {{ padding: 15px 30px; background: #3498db; color: white; border: none; border-radius: 10px; font-size: 18px; cursor: pointer; text-decoration: none; display: inline-block; margin: 10px; }}
            </style>
            <script>
                setTimeout(function() {{
                    window.location.href = '/emergency/competition/';
                }}, 3000);
            </script>
        </head>
        <body>
            <div class="card">
                <div class="result">{'🎉' if is_correct else '❌'}</div>
                <h1 style="color: #2c3e50;">{'إجابة صحيحة!' if is_correct else 'إجابة خاطئة'}</h1>
                <p style="font-size: 1.2em; margin: 20px 0;">
                    السؤال: {question} = {correct_answer}
                </p>
                {'<p style="color: #27ae60;">أحسنت! إجابتك صحيحة</p>' if is_correct else f'<p style="color: #e74c3c;">إجابتك: {student_answer}<br>الإجابة الصحيحة: {correct_answer}</p>'}
                
                <div style="margin: 30px 0;">
                    <a href="/emergency/competition/" class="btn">➡️ السؤال التالي</a>
                    <a href="/emergency/student/" class="btn">🔙 العودة للبداية</a>
                </div>
                
                <p style="color: #7f8c8d; font-size: 0.9em;">سيتم الانتقال للسؤال التالي خلال 3 ثوان...</p>
            </div>
        </body>
        </html>
        """)
    
    return redirect('/emergency/competition/')
