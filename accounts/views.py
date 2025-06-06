from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
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
    # إنشاء ملف المعلم إذا لم يكن موجود
    profile, created = TeacherProfile.objects.get_or_create(user=request.user)
    
    context = {
        'teacher': request.user,
        'profile': profile,
        'recent_sessions': StudentSession.objects.filter(is_active=True)[:10]
    }
    return render(request, 'accounts/teacher_dashboard.html', context)


def teacher_logout(request):
    """تسجيل خروج المعلم"""
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    return redirect('teacher_login')
