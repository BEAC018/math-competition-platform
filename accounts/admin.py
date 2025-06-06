from django.contrib import admin
from .models import TeacherProfile, StudentSession


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'school_name', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'school_name']


@admin.register(StudentSession)
class StudentSessionAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'grade_level', 'access_code', 'session_start', 'is_active']
    list_filter = ['grade_level', 'is_active', 'session_start']
    search_fields = ['student_name']
    readonly_fields = ['session_start']
