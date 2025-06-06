from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.http import HttpResponse


@login_required
def dashboard_home(request):
    """الصفحة الرئيسية للوحة التحكم"""
    try:
        from competitions.models import Competition, Answer
        from accounts.models import StudentSession

        # إحصائيات عامة
        total_competitions = Competition.objects.count()
        completed_competitions = Competition.objects.filter(is_completed=True).count()
        active_sessions = StudentSession.objects.filter(is_active=True).count()
        average_score = Competition.objects.filter(is_completed=True).aggregate(
            avg_score=Avg('score')
        )['avg_score'] or 0

        # إحصائيات حسب المستوى
        grade_stats = Competition.objects.filter(is_completed=True).values('grade_level').annotate(
            count=Count('id'),
            avg_score=Avg('score')
        ).order_by('grade_level')

        # آخر المسابقات
        recent_competitions = Competition.objects.filter(is_completed=True).order_by('-end_time')[:10]

        context = {
            'total_competitions': total_competitions,
            'completed_competitions': completed_competitions,
            'active_sessions': active_sessions,
            'average_score': round(average_score, 2),
            'grade_stats': grade_stats,
            'recent_competitions': recent_competitions,
        }

        return render(request, 'dashboard/home.html', context)

    except Exception as e:
        # في حالة عدم وجود جداول قاعدة البيانات بعد
        return HttpResponse(f"""
        <div style="text-align: center; padding: 50px; font-family: Arial;">
            <h2>📊 لوحة التحكم</h2>
            <p>جاري إعداد قاعدة البيانات...</p>
            <p>يرجى إعادة النشر أو تشغيل migrations</p>
            <p style="color: #e74c3c;">خطأ: {str(e)}</p>
            <a href="/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">العودة للرئيسية</a>
        </div>
        """)


@login_required
def competition_analytics(request):
    """تحليلات المسابقات"""
    try:
        from competitions.models import Competition

        # إحصائيات مفصلة
        competitions = Competition.objects.filter(is_completed=True)

        # توزيع النتائج
        score_ranges = {
            'excellent': competitions.filter(score__gte=90).count(),
            'good': competitions.filter(score__gte=70, score__lt=90).count(),
            'average': competitions.filter(score__gte=50, score__lt=70).count(),
            'poor': competitions.filter(score__lt=50).count(),
        }

        # أداء حسب نوع العملية (سيتم تطويره لاحقاً)
        operation_stats = {}

        context = {
            'competitions': competitions,
            'score_ranges': score_ranges,
            'operation_stats': operation_stats,
        }

        return render(request, 'dashboard/analytics.html', context)

    except Exception as e:
        return HttpResponse(f"""
        <div style="text-align: center; padding: 50px; font-family: Arial;">
            <h2>📈 تحليلات المسابقات</h2>
            <p>جاري إعداد قاعدة البيانات...</p>
            <p style="color: #e74c3c;">خطأ: {str(e)}</p>
            <a href="/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">العودة للرئيسية</a>
        </div>
        """)


@login_required
def student_reports(request):
    """تقارير الطلاب"""
    try:
        from competitions.models import Competition

        competitions = Competition.objects.filter(is_completed=True).order_by('-end_time')

        # فلترة حسب المستوى إذا تم تحديده
        grade_filter = request.GET.get('grade')
        if grade_filter:
            competitions = competitions.filter(grade_level=grade_filter)

        # الحصول على قائمة المستويات المتاحة
        available_grades = Competition.objects.values_list('grade_level', flat=True).distinct()

        context = {
            'competitions': competitions,
            'available_grades': available_grades,
            'selected_grade': grade_filter,
        }

        return render(request, 'dashboard/reports.html', context)

    except Exception as e:
        return HttpResponse(f"""
        <div style="text-align: center; padding: 50px; font-family: Arial;">
            <h2>📋 تقارير الطلاب</h2>
            <p>جاري إعداد قاعدة البيانات...</p>
            <p style="color: #e74c3c;">خطأ: {str(e)}</p>
            <a href="/" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">العودة للرئيسية</a>
        </div>
        """)
