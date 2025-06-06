from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from .models import StudentSession, TeacherProfile


def teacher_login(request):
    """صفحة دخول المعلمين"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    
    return render(request, 'accounts/teacher_login.html')


def student_login(request):
    """صفحة دخول الطلاب"""
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        access_code = request.POST.get('access_code')
        grade_level = request.POST.get('grade_level')
        
        # التحقق من رمز الدخول
        if access_code == settings.STUDENT_ACCESS_CODE:
            # إنشاء جلسة طالب جديدة
            session = StudentSession.objects.create(
                student_name=student_name,
                access_code=access_code,
                grade_level=grade_level
            )
            
            # حفظ معلومات الطالب في الجلسة
            request.session['student_id'] = session.id
            request.session['student_name'] = student_name
            request.session['grade_level'] = grade_level
            
            return redirect('competition_start')
        else:
            messages.error(request, 'رمز الدخول غير صحيح')
    
    return render(request, 'accounts/student_login.html')


@login_required
def teacher_dashboard(request):
    """لوحة تحكم المعلم"""
    try:
        # إنشاء ملف المعلم إذا لم يكن موجود
        profile, created = TeacherProfile.objects.get_or_create(user=request.user)

        # الحصول على آخر الجلسات
        recent_sessions = StudentSession.objects.filter(is_active=True)[:10]

        context = {
            'teacher': request.user,
            'profile': profile,
            'recent_sessions': recent_sessions
        }
        return render(request, 'accounts/teacher_dashboard.html', context)

    except Exception as e:
        return HttpResponse(f"""
        <div style="text-align: center; padding: 50px; font-family: Arial;">
            <h2>👨‍🏫 لوحة تحكم المعلم</h2>
            <p>مرحباً {request.user.get_full_name() or request.user.username}</p>
            <p>جاري إعداد قاعدة البيانات...</p>
            <p style="color: #e74c3c;">خطأ: {str(e)}</p>
            <div style="margin: 20px 0;">
                <a href="/dashboard/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px;">📊 لوحة التحكم</a>
                <a href="/admin/" style="background: #e74c3c; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px;">⚙️ لوحة الإدارة</a>
                <a href="/" style="background: #27ae60; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px;">🏠 الرئيسية</a>
            </div>
        </div>
        """)


def teacher_logout(request):
    """تسجيل خروج المعلم"""
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    return redirect('teacher_login')


def create_admin(request):
    """إنشاء مدير تلقائ<|im_start|> - للاستخدام مرة واحدة فقط"""
    try:
        # التحقق من وجود مدير
        if User.objects.filter(is_superuser=True).exists():
            return HttpResponse("""
            <div style="text-align: center; padding: 50px; font-family: Arial;">
                <h2>✅ يوجد مدير بالفعل</h2>
                <p>تم إنشاء حساب المدير مسبقاً</p>
                <p><strong>اسم المستخدم:</strong> admin</p>
                <p><strong>كلمة المرور:</strong> admin123456</p>
                <a href="/accounts/login/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">دخول المعلمين</a>
            </div>
            """)

        # إنشاء مدير جديد
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@mathcompetition.com',
            password='admin123456',
            first_name='مدير',
            last_name='النظام'
        )

        return HttpResponse("""
        <div style="text-align: center; padding: 50px; font-family: Arial;">
            <h2>🎉 تم إنشاء المدير بنجاح!</h2>
            <p><strong>اسم المستخدم:</strong> admin</p>
            <p><strong>كلمة المرور:</strong> admin123456</p>
            <p>يمكنك الآن الدخول كمعلم أو مدير</p>
            <a href="/accounts/login/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">دخول المعلمين</a>
            <a href="/admin/" style="background: #e74c3c; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-left: 10px;">لوحة الإدارة</a>
        </div>
        """)

    except Exception as e:
        return HttpResponse(f"""
        <div style="text-align: center; padding: 50px; font-family: Arial;">
            <h2>❌ خطأ في إنشاء المدير</h2>
            <p>{str(e)}</p>
            <a href="/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">العودة للرئيسية</a>
        </div>
        """)
