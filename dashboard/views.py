from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from competitions.models import Competition, Answer
from accounts.models import StudentSession


@login_required
def dashboard_home(request):
    """الصفحة الرئيسية للوحة التحكم"""
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


@login_required
def competition_analytics(request):
    """تحليلات المسابقات"""
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


@login_required
def student_reports(request):
    """تقارير الطلاب"""
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
