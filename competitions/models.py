from django.db import models
import random


class Question(models.Model):
    """نموذج الأسئلة الرياضية"""
    OPERATION_CHOICES = [
        ('addition', 'الجمع'),
        ('subtraction', 'الطرح'),
        ('multiplication', 'الضرب'),
        ('division', 'القسمة'),
        ('mixed', 'مختلط'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'سهل'),
        ('medium', 'متوسط'),
        ('hard', 'صعب'),
    ]
    
    operation_type = models.CharField(max_length=20, choices=OPERATION_CHOICES, verbose_name="نوع العملية")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, verbose_name="مستوى الصعوبة")
    question_text = models.TextField(verbose_name="نص السؤال")
    correct_answer = models.IntegerField(verbose_name="الإجابة الصحيحة")
    grade_level = models.CharField(max_length=50, verbose_name="المستوى الدراسي")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "سؤال"
        verbose_name_plural = "الأسئلة"
    
    def __str__(self):
        return f"{self.question_text} = {self.correct_answer}"


class Competition(models.Model):
    """نموذج المسابقة"""
    student_name = models.CharField(max_length=100, verbose_name="اسم الطالب")
    grade_level = models.CharField(max_length=50, verbose_name="المستوى الدراسي")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="وقت البداية")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="وقت الانتهاء")
    total_questions = models.IntegerField(default=10, verbose_name="عدد الأسئلة")
    correct_answers = models.IntegerField(default=0, verbose_name="الإجابات الصحيحة")
    is_completed = models.BooleanField(default=False, verbose_name="مكتملة")
    score = models.FloatField(default=0.0, verbose_name="النتيجة")
    
    class Meta:
        verbose_name = "مسابقة"
        verbose_name_plural = "المسابقات"
    
    def __str__(self):
        return f"مسابقة {self.student_name} - {self.grade_level}"
    
    def calculate_score(self):
        """حساب النتيجة"""
        if self.total_questions > 0:
            self.score = (self.correct_answers / self.total_questions) * 100
        return self.score


class Answer(models.Model):
    """نموذج الإجابات"""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name="المسابقة")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="السؤال")
    student_answer = models.IntegerField(verbose_name="إجابة الطالب")
    is_correct = models.BooleanField(verbose_name="صحيحة")
    answer_time = models.DateTimeField(auto_now_add=True, verbose_name="وقت الإجابة")
    
    class Meta:
        verbose_name = "إجابة"
        verbose_name_plural = "الإجابات"
    
    def __str__(self):
        return f"إجابة {self.competition.student_name} - {self.question.question_text}"
