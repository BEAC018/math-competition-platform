from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.competition_start, name='competition_start'),
    path('question/', views.get_question, name='get_question'),
    path('submit/', views.submit_answer, name='submit_answer'),
    path('results/', views.competition_results, name='competition_results'),
]
