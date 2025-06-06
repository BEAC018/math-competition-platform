from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.teacher_logout, name='teacher_logout'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/login/', views.student_login, name='student_login'),
    path('create-admin/', views.create_admin, name='create_admin'),
]
