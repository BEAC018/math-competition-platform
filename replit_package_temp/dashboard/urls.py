from django.urls import path
from . import views
from .dashboard_utils import execute_start_script

app_name = 'dashboard'

urlpatterns = [
    # Admin dashboard routes
    path('', views.dashboard_home, name='home'),
    path('students/', views.students_list, name='students'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    
    # Statistics routes
    path('stats/grades/', views.grade_statistics, name='grade_stats'),
    path('stats/operations/', views.operation_statistics, name='operation_stats'),
    path('stats/difficulty/', views.difficulty_statistics, name='difficulty_stats'),
    path('stats/overall/', views.overall_statistics, name='overall_stats'),
    
    # Data management routes
    path('manage/students/', views.manage_students, name='manage_students'),
    path('manage/grades/', views.manage_grades, name='manage_grades'),
    path('manage/reset-results/', views.reset_results, name='reset_results'),
    
    # AJAX routes for charts and data
    path('api/chart-data/<str:chart_type>/', views.chart_data, name='chart_data'),
    
    # Auto-start application
    path('execute-start-script/', execute_start_script, name='execute_start_script'),
]