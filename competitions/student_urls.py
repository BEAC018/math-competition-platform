from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    # Student authentication and setup
    path('login/', views.student_login, name='login'),
    path('setup/', views.student_setup, name='setup'),

    # Student competition
    path('competition/', views.student_competition, name='competition'),
    path('api/get-question/', views.student_get_question, name='get_question'),
    path('api/submit-answer/', views.student_submit_answer, name='submit_answer'),
    path('finish/', views.student_finish_competition, name='finish'),

    # Student results
    path('results/', views.student_results, name='results'),
]
