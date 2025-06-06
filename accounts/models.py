from django.db import models
from django.contrib.auth.models import User


class TeacherProfile(models.Model):
    """ملف المعلم الشخصي"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    school_name = models.CharField(max_length=200, verbose_name="اسم المدرسة", blank=True)
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "ملف المعلم"
        verbose_name_plural = "ملفات المعلمين"
    
    def __str__(self):
        return f"المعلم: {self.user.get_full_name() or self.user.username}"


class StudentSession(models.Model):
    """جلسة الطالب"""
    student_name = models.CharField(max_length=100, verbose_name="اسم الطالب")
    access_code = models.CharField(max_length=20, verbose_name="رمز الدخول")
    grade_level = models.CharField(max_length=50, verbose_name="المستوى الدراسي")
    session_start = models.DateTimeField(auto_now_add=True, verbose_name="بداية الجلسة")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    
    class Meta:
        verbose_name = "جلسة طالب"
        verbose_name_plural = "جلسات الطلاب"
    
    def __str__(self):
        return f"{self.student_name} - {self.grade_level}"
