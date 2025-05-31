from django.urls import path
from . import views

app_name = 'competitions'

urlpatterns = [
    # Home page and general routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Competition routes
    path('start/', views.start_competition, name='start_competition'),
    path('question/<int:question_number>/', views.question, name='question'),
    path('submit-answer/<int:question_number>/', views.submit_answer, name='submit_answer'),
    path('results/<int:competition_id>/', views.results, name='results'),

    # Student profile and history
    path('history/', views.competition_history, name='history'),

    # Advanced analytics
    path('analytics/', views.advanced_analytics, name='advanced_analytics'),
    path('participant/<int:participant_id>/', views.participant_profile, name='participant_profile'),

    # Participant management
    path('add-participant/', views.add_participant, name='add_participant'),
    path('delete-participant/<int:participant_id>/', views.delete_participant, name='delete_participant'),
    path('delete-multiple-participants/', views.delete_multiple_participants, name='delete_multiple_participants'),

    path('delete-multiple-participants/', views.delete_multiple_participants, name='delete_multiple_participants'),
    path('clear-all-participants/', views.clear_all_participants, name='clear_all_participants'),
    path('get-participants-by-grade/', views.get_participants_by_grade, name='get_participants_by_grade'),

    # Competition history management
    path('clear-history/', views.clear_competition_history, name='clear_competition_history'),

    # Export data
    path('export-excel/', views.export_results_excel, name='export_results_excel'),
    path('export-analytics-pdf/', views.export_analytics_pdf, name='export_analytics_pdf'),
    path('export-analytics-excel/', views.export_analytics_excel, name='export_analytics_excel'),
    path('export-history-excel/', views.export_history_excel, name='export_history_excel'),
    path('export-history-pdf/', views.export_history_pdf, name='export_history_pdf'),

    # Individual analytics exports
    path('export-grade-analytics/', views.export_grade_analytics_excel, name='export_grade_analytics_excel'),
    path('export-operations-analytics/', views.export_operations_analytics_excel, name='export_operations_analytics_excel'),
    path('export-general-analytics/', views.export_general_analytics_excel, name='export_general_analytics_excel'),
    path('export-participants-results/', views.export_participants_results_excel, name='export_participants_results_excel'),

    # Chart data API endpoints
    path('api/chart-data/<str:chart_type>/', views.get_chart_data, name='get_chart_data'),

    # Competition actions
    path('repeat/<int:competition_id>/', views.repeat_competition, name='repeat_competition'),

    # Testing and demo
    path('score-test/', views.score_test, name='score_test'),

    # Student Analytics for Teachers
    path('student-analytics/', views.student_analytics, name='student_analytics'),
    path('student-session/<int:session_id>/', views.student_session_detail, name='student_session_detail'),
    path('export-student-session-excel/<int:session_id>/', views.export_student_session_excel, name='export_student_session_excel'),
    path('export-student-session-pdf/<int:session_id>/', views.export_student_session_pdf, name='export_student_session_pdf'),
]