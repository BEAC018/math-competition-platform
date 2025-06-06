from django.contrib import admin
from .models import Question, Competition, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'correct_answer', 'operation_type', 'difficulty', 'grade_level']
    list_filter = ['operation_type', 'difficulty', 'grade_level']
    search_fields = ['question_text']


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'grade_level', 'start_time', 'is_completed', 'score']
    list_filter = ['grade_level', 'is_completed', 'start_time']
    search_fields = ['student_name']
    readonly_fields = ['start_time', 'score']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['competition', 'question', 'student_answer', 'is_correct', 'answer_time']
    list_filter = ['is_correct', 'answer_time']
    search_fields = ['competition__student_name']
