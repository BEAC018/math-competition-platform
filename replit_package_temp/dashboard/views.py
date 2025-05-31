from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Max, F, Q, Case, When, IntegerField
from django.utils import timezone
from django.contrib.auth.models import User

from datetime import timedelta
import json

from accounts.models import Profile
from competitions.models import Competition, MathQuestion, UserResponse, CompetitionResult
from .models import StatisticsCache
import subprocess
import os
import sys
import platform

# Check if user is an admin
def is_admin(user):
    if not user.is_authenticated:
        return False
    try:
        return user.profile.is_admin
    except Profile.DoesNotExist:
        return False

# Admin-only decorator
def admin_required(view_func):
    decorated_view = user_passes_test(is_admin, login_url='accounts:login')(view_func)
    return login_required(decorated_view)

@admin_required
def dashboard_home(request):
    """Dashboard home page with overview statistics"""
    # Get some basic statistics
    total_students = Profile.objects.filter(user_type='student').count()
    total_competitions = Competition.objects.filter(is_completed=True).count()

    # Get competitions per day (last 7 days)
    last_week = timezone.now() - timedelta(days=7)
    competitions_per_day = Competition.objects.filter(
        is_completed=True,
        end_time__gte=last_week
    ).extra(
        select={'day': 'DATE(end_time)'}
    ).values('day').annotate(count=Count('id')).order_by('day')

    # Get average scores by grade level
    avg_scores_by_grade = CompetitionResult.objects.select_related(
        'competition__user__profile'
    ).filter(
        competition__user__profile__grade__isnull=False
    ).values(
        'competition__user__profile__grade'
    ).annotate(
        avg_score=Avg('total_score')
    ).order_by('competition__user__profile__grade')

    # Recent competitions
    recent_competitions = Competition.objects.filter(
        is_completed=True
    ).select_related('user').order_by('-end_time')[:10]

    context = {
        'total_students': total_students,
        'total_competitions': total_competitions,
        'competitions_per_day': competitions_per_day,
        'avg_scores_by_grade': avg_scores_by_grade,
        'recent_competitions': recent_competitions,
    }
    return render(request, 'dashboard/home.html', context)

@admin_required
def students_list(request):
    """List all students"""
    # Get all student profiles
    students = Profile.objects.filter(
        user_type='student'
    ).select_related('user').order_by('user__first_name', 'user__last_name')

    # Add some statistics to each student
    for student in students:
        student.competition_count = Competition.objects.filter(
            user=student.user,
            is_completed=True
        ).count()

        if student.competition_count > 0:
            # Get the student's average score
            student.avg_score = CompetitionResult.objects.filter(
                competition__user=student.user
            ).aggregate(avg=Avg('total_score'))['avg']

            # Get the student's best score
            student.best_score = CompetitionResult.objects.filter(
                competition__user=student.user
            ).aggregate(max=Max('total_score'))['max']
        else:
            student.avg_score = 0
            student.best_score = 0

    context = {
        'students': students,
    }
    return render(request, 'dashboard/students_list.html', context)

@admin_required
def student_detail(request, student_id):
    """View detailed statistics for a student"""
    # Get the student profile
    student = get_object_or_404(Profile, user_id=student_id, user_type='student')

    # Get all competitions for this student
    competitions = Competition.objects.filter(
        user=student.user,
        is_completed=True
    ).order_by('-end_time')

    # Calculate operation-specific statistics
    operation_stats = UserResponse.objects.filter(
        competition__user=student.user,
        competition__is_completed=True
    ).values(
        'question__operation'
    ).annotate(
        total=Count('id'),
        correct=Sum(
            Case(
                When(is_correct=True, then=1),
                default=0,
                output_field=IntegerField()
            )
        )
    )

    # Convert to percentages
    for stat in operation_stats:
        if stat['total'] > 0:
            stat['percentage'] = (stat['correct'] / stat['total']) * 100
        else:
            stat['percentage'] = 0

    # Calculate difficulty-specific statistics
    difficulty_stats = competitions.values(
        'difficulty'
    ).annotate(
        count=Count('id'),
        avg_score=Avg('result__total_score')
    ).order_by('difficulty')

    context = {
        'student': student,
        'competitions': competitions,
        'operation_stats': operation_stats,
        'difficulty_stats': difficulty_stats,
    }
    return render(request, 'dashboard/student_detail.html', context)

@admin_required
def grade_statistics(request):
    """View statistics by grade level"""
    # Get statistics by grade
    grade_stats = Profile.objects.filter(
        user_type='student',
        grade__isnull=False
    ).values(
        'grade'
    ).annotate(
        student_count=Count('id')
    ).order_by('grade')

    # Get average scores by grade
    grade_scores = CompetitionResult.objects.select_related(
        'competition__user__profile'
    ).filter(
        competition__user__profile__grade__isnull=False
    ).values(
        'competition__user__profile__grade'
    ).annotate(
        avg_score=Avg('total_score'),
        competition_count=Count('id')
    ).order_by('competition__user__profile__grade')

    # Merge the two datasets
    for grade in grade_stats:
        for score in grade_scores:
            if grade['grade'] == score['competition__user__profile__grade']:
                grade['avg_score'] = score['avg_score']
                grade['competition_count'] = score['competition_count']
                break
        else:
            grade['avg_score'] = 0
            grade['competition_count'] = 0

    context = {
        'grade_stats': grade_stats,
    }
    return render(request, 'dashboard/grade_statistics.html', context)

@admin_required
def operation_statistics(request):
    """View statistics by operation type"""
    # Get statistics for each operation type
    operation_stats = UserResponse.objects.values(
        'question__operation'
    ).annotate(
        total=Count('id'),
        correct=Sum(
            Case(
                When(is_correct=True, then=1),
                default=0,
                output_field=IntegerField()
            )
        )
    )

    # Calculate percentages
    for stat in operation_stats:
        if stat['total'] > 0:
            stat['percentage'] = (stat['correct'] / stat['total']) * 100
        else:
            stat['percentage'] = 0

    # Get statistics by difficulty level for each operation
    operation_by_difficulty = UserResponse.objects.values(
        'question__operation',
        'question__difficulty'
    ).annotate(
        total=Count('id'),
        correct=Sum(
            Case(
                When(is_correct=True, then=1),
                default=0,
                output_field=IntegerField()
            )
        )
    ).order_by('question__operation', 'question__difficulty')

    # Calculate percentages
    for stat in operation_by_difficulty:
        if stat['total'] > 0:
            stat['percentage'] = (stat['correct'] / stat['total']) * 100
        else:
            stat['percentage'] = 0

    context = {
        'operation_stats': operation_stats,
        'operation_by_difficulty': operation_by_difficulty,
    }
    return render(request, 'dashboard/operation_statistics.html', context)

@admin_required
def difficulty_statistics(request):
    """View statistics by difficulty level"""
    # Get statistics for each difficulty level
    difficulty_stats = Competition.objects.filter(
        is_completed=True
    ).values(
        'difficulty'
    ).annotate(
        count=Count('id'),
        avg_score=Avg('result__total_score')
    ).order_by('difficulty')

    # Get the percentage of students who chose each difficulty level
    total_competitions = Competition.objects.filter(is_completed=True).count()
    for stat in difficulty_stats:
        if total_competitions > 0:
            stat['percentage'] = (stat['count'] / total_competitions) * 100
        else:
            stat['percentage'] = 0

    context = {
        'difficulty_stats': difficulty_stats,
        'total_competitions': total_competitions,
    }
    return render(request, 'dashboard/difficulty_statistics.html', context)

@admin_required
def overall_statistics(request):
    """View overall system statistics"""
    # Get general statistics
    total_students = Profile.objects.filter(user_type='student').count()
    total_competitions = Competition.objects.filter(is_completed=True).count()
    total_questions = UserResponse.objects.count()
    total_correct = UserResponse.objects.filter(is_correct=True).count()

    # Calculate overall correct percentage
    overall_percentage = 0
    if total_questions > 0:
        overall_percentage = (total_correct / total_questions) * 100

    # Get statistics by time period
    today = timezone.now().date()
    competitions_today = Competition.objects.filter(
        is_completed=True,
        end_time__date=today
    ).count()

    last_week = timezone.now() - timedelta(days=7)
    competitions_last_week = Competition.objects.filter(
        is_completed=True,
        end_time__gte=last_week
    ).count()

    # Get statistics for each month (compatible with SQLite and PostgreSQL)
    from django.db.models.functions import TruncMonth

    monthly_stats = Competition.objects.filter(
        is_completed=True
    ).annotate(
        month=TruncMonth('end_time')
    ).values('month').annotate(
        count=Count('id'),
        avg_score=Avg('result__total_score')
    ).order_by('month')

    context = {
        'total_students': total_students,
        'total_competitions': total_competitions,
        'total_questions': total_questions,
        'total_correct': total_correct,
        'overall_percentage': overall_percentage,
        'competitions_today': competitions_today,
        'competitions_last_week': competitions_last_week,
        'monthly_stats': monthly_stats,
    }
    return render(request, 'dashboard/overall_statistics.html', context)

@admin_required
def manage_students(request):
    """Manage student accounts"""
    # This is just a placeholder view, we'll implement the actual form handling later
    students = User.objects.filter(profile__user_type='student').select_related('profile')

    context = {
        'students': students,
    }
    return render(request, 'dashboard/manage_students.html', context)

@admin_required
def manage_grades(request):
    """Manage grade levels"""
    # This is just a placeholder view, we'll implement the actual form handling later
    # For now, we'll just show the distribution of students by grade
    grade_distribution = Profile.objects.filter(
        user_type='student',
        grade__isnull=False
    ).values('grade').annotate(count=Count('id')).order_by('grade')

    context = {
        'grade_distribution': grade_distribution,
    }
    return render(request, 'dashboard/manage_grades.html', context)

@admin_required
def reset_results(request):
    """Reset competition results"""
    if request.method == 'POST':
        # Get the reset type
        reset_type = request.POST.get('reset_type', 'none')

        if reset_type == 'all':
            # Delete all competition results
            CompetitionResult.objects.all().delete()
            # Delete all competitions (which will cascade to user responses)
            Competition.objects.all().delete()
            messages.success(request, 'تم إعادة ضبط جميع النتائج بنجاح')

        elif reset_type == 'student':
            # Reset for a specific student
            student_id = request.POST.get('student_id')
            if student_id:
                user = get_object_or_404(User, id=student_id)
                # Delete all competition results for this user
                CompetitionResult.objects.filter(competition__user=user).delete()
                # Delete all competitions for this user
                Competition.objects.filter(user=user).delete()
                messages.success(request, f'تم إعادة ضبط نتائج الطالب {user.first_name} {user.last_name} بنجاح')

        elif reset_type == 'grade':
            # Reset for a specific grade
            grade = request.POST.get('grade')
            if grade:
                # Get all users in this grade
                users = User.objects.filter(profile__grade=grade)
                # Delete all competition results for these users
                CompetitionResult.objects.filter(competition__user__in=users).delete()
                # Delete all competitions for these users
                Competition.objects.filter(user__in=users).delete()
                messages.success(request, f'تم إعادة ضبط نتائج الصف {grade} بنجاح')

        else:
            messages.error(request, 'نوع إعادة الضبط غير صالح')

        return redirect('dashboard:home')

    # Get all students for the form
    students = User.objects.filter(profile__user_type='student').select_related('profile')

    # Get all grades for the form
    grades = Profile.objects.filter(
        user_type='student',
        grade__isnull=False
    ).values_list('grade', flat=True).distinct().order_by('grade')

    context = {
        'students': students,
        'grades': grades,
    }
    return render(request, 'dashboard/reset_results.html', context)

@admin_required
def chart_data(request, chart_type):
    """AJAX endpoint to get data for charts"""
    # Check if we have this data in the cache
    cache_key = chart_type
    cached_data = StatisticsCache.get_cache('chart_data', cache_key)
    if cached_data:
        return JsonResponse(cached_data)

    # If not in cache, generate the data
    data = {}

    if chart_type == 'competitions_by_day':
        # Get competitions per day (last 30 days)
        last_month = timezone.now() - timedelta(days=30)
        competitions = Competition.objects.filter(
            is_completed=True,
            end_time__gte=last_month
        ).extra(
            select={'day': 'DATE(end_time)'}
        ).values('day').annotate(count=Count('id')).order_by('day')

        # Format the data for Chart.js
        labels = [comp['day'].strftime('%Y-%m-%d') for comp in competitions]
        values = [comp['count'] for comp in competitions]

        data = {
            'labels': labels,
            'datasets': [{
                'label': 'عدد المسابقات',
                'data': values,
                'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            }]
        }

    elif chart_type == 'scores_by_grade':
        # Get average scores by grade
        scores = CompetitionResult.objects.select_related(
            'competition__user__profile'
        ).filter(
            competition__user__profile__grade__isnull=False
        ).values(
            'competition__user__profile__grade'
        ).annotate(
            avg_score=Avg('total_score')
        ).order_by('competition__user__profile__grade')

        # Format the data for Chart.js
        labels = [f'الصف {score["competition__user__profile__grade"]}' for score in scores]
        values = [score['avg_score'] for score in scores]

        data = {
            'labels': labels,
            'datasets': [{
                'label': 'متوسط الدرجات',
                'data': values,
                'backgroundColor': 'rgba(75, 192, 192, 0.5)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }]
        }

    elif chart_type == 'operation_success':
        # Get success rate by operation
        operations = UserResponse.objects.values(
            'question__operation'
        ).annotate(
            total=Count('id'),
            correct=Sum(
                Case(
                    When(is_correct=True, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )

        # Calculate percentages
        labels = []
        values = []
        colors = [
            'rgba(255, 99, 132, 0.5)',
            'rgba(54, 162, 235, 0.5)',
            'rgba(255, 206, 86, 0.5)',
            'rgba(75, 192, 192, 0.5)'
        ]

        operation_names = {
            'addition': 'جمع',
            'subtraction': 'طرح',
            'multiplication': 'ضرب',
            'division': 'قسمة',
        }

        for op in operations:
            if op['total'] > 0:
                percentage = (op['correct'] / op['total']) * 100
                op_name = operation_names.get(op['question__operation'], op['question__operation'])
                labels.append(op_name)
                values.append(percentage)

        data = {
            'labels': labels,
            'datasets': [{
                'label': 'نسبة النجاح (%)',
                'data': values,
                'backgroundColor': colors[:len(labels)],
                'borderColor': [color.replace('0.5', '1') for color in colors[:len(labels)]],
                'borderWidth': 1
            }]
        }

    # Cache the data
    StatisticsCache.set_cache('chart_data', cache_key, data)

    return JsonResponse(data)

@admin_required
def execute_start_script(request):
    """Execute the start_django script to start the application automatically"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'طريقة غير مسموح بها'}, status=405)

    try:
        # Check if the request is AJAX
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = json.loads(request.body)
            if data.get('action') != 'start':
                return JsonResponse({'success': False, 'error': 'إجراء غير صالح'}, status=400)

        # Determine which script to run based on the OS
        is_windows = platform.system() == 'Windows'
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  'start_django.bat' if is_windows else 'start_django.sh')

        # Make sure the script exists
        if not os.path.exists(script_path):
            return JsonResponse({'success': False, 'error': 'ملف بدء التشغيل غير موجود'}, status=404)

        # Make the script executable on Unix-like systems
        if not is_windows:
            try:
                os.chmod(script_path, 0o755)  # rwx for owner, rx for group and others
            except Exception as e:
                return JsonResponse({'success': False, 'error': f'فشل تعيين صلاحيات التنفيذ: {str(e)}'}, status=500)

        # Execute the script
        if is_windows:
            # On Windows, start the script in a new console window
            subprocess.Popen(['start', 'cmd', '/k', script_path], shell=True)
        else:
            # On Unix-like systems, run the script in the background
            subprocess.Popen([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=True, start_new_session=True)

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
