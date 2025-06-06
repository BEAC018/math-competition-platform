from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('analytics/', views.competition_analytics, name='competition_analytics'),
    path('reports/', views.student_reports, name='student_reports'),
]
