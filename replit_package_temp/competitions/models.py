from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
import random
import json
import logging

logger = logging.getLogger('competitions')

class Participant(models.Model):
    """
    Model for storing participant information.
    """
    GRADE_CHOICES = [
        (1, "الأول ابتدائي"),
        (2, "الثاني ابتدائي"),
        (3, "الثالث ابتدائي"),
        (4, "الرابع ابتدائي"),
        (5, "الخامس ابتدائي"),
        (6, "السادس ابتدائي"),
        (7, "الأول إعدادي"),
        (8, "الثاني إعدادي"),
        (9, "الثالث إعدادي"),
    ]

    GROUP_CHOICES = [
        (1, "الفوج الأول"),
        (2, "الفوج الثاني"),
    ]

    name = models.CharField(max_length=100, verbose_name="الاسم الكامل")
    grade = models.IntegerField(verbose_name="الصف الدراسي", choices=GRADE_CHOICES)
    group = models.IntegerField(verbose_name="الفوج", choices=GROUP_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        verbose_name = "مشارك"
        verbose_name_plural = "المشاركون"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.get_grade_display()}"

    def clean(self):
        """التحقق من صحة البيانات"""
        if not self.name or len(self.name.strip()) < 2:
            raise ValidationError('يجب أن يكون الاسم أطول من حرفين')

        # التحقق من عدم وجود اسم مكرر في نفس المستوى والفوج
        if Participant.objects.filter(
            name=self.name,
            grade=self.grade,
            group=self.group
        ).exclude(pk=self.pk).exists():
            raise ValidationError('يوجد مشارك بنفس الاسم في نفس المستوى والفوج')

    def save(self, *args, **kwargs):
        """حفظ محسن مع تسجيل"""
        self.full_clean()
        logger.info(f"إضافة/تحديث مشارك: {self.name} - {self.get_grade_display()}")
        super().save(*args, **kwargs)

    @property
    def initials(self):
        """الأحرف الأولى من الاسم"""
        parts = self.name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}"
        return self.name[0] if self.name else "؟"

    @property
    def competitions_count(self):
        """عدد المسابقات التي شارك فيها"""
        return self.competitions.count()

    @property
    def average_score(self):
        """متوسط النقاط"""
        results = [comp.result.total_score for comp in self.competitions.filter(is_completed=True) if hasattr(comp, 'result')]
        return sum(results) / len(results) if results else 0

    @property
    def best_score(self):
        """أفضل نتيجة"""
        results = [comp.result.total_score for comp in self.competitions.filter(is_completed=True) if hasattr(comp, 'result')]
        return max(results) if results else 0

    @classmethod
    def get_by_grade(cls, grade):
        """الحصول على المشاركين حسب المستوى"""
        return cls.objects.filter(grade=grade).order_by('name')

    @classmethod
    def get_statistics(cls):
        """إحصائيات عامة للمشاركين"""
        total = cls.objects.count()
        by_grade = {}
        for grade, name in cls.GRADE_CHOICES:
            count = cls.objects.filter(grade=grade).count()
            if count > 0:
                by_grade[grade] = {'name': name, 'count': count}

        return {
            'total': total,
            'by_grade': by_grade,
            'active_grades': len(by_grade)
        }

class MathQuestion(models.Model):
    """
    Model for storing math questions for the competition.
    """
    OPERATION_CHOICES = [
        ('addition', 'جمع'),
        ('subtraction', 'طرح'),
        ('multiplication', 'ضرب'),
        ('division', 'قسمة'),
        ('mixed_operations', 'عمليات مختلطة'),
        ('fractions', 'كسور وأعداد عشرية'),
        ('algebra', 'جبر'),
        ('geometry', 'هندسة'),
        ('trigonometry', 'مثلثات'),
        ('word_problems', 'مسائل تطبيقية'),
    ]

    # المرحلة الأولى - المستويات الأساسية (1-6)
    STAGE_1_CHOICES = [
        (1, 'المستوى الأول - المرحلة الأولى'),
        (2, 'المستوى الثاني - المرحلة الأولى'),
        (3, 'المستوى الثالث - المرحلة الأولى'),
        (4, 'المستوى الرابع - المرحلة الأولى'),
        (5, 'المستوى الخامس - المرحلة الأولى'),
        (6, 'المستوى السادس - المرحلة الأولى'),
    ]

    # المرحلة الثانية - المستويات المتقدمة
    STAGE_2_CHOICES = [
        (7, 'المستوى الأول - المرحلة الثانية'),
        (8, 'المستوى الثاني - المرحلة الثانية'),
        (9, 'المستوى الثالث - المرحلة الثانية'),
    ]

    # دمج جميع المستويات
    DIFFICULTY_CHOICES = STAGE_1_CHOICES + STAGE_2_CHOICES

    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(9)])
    first_number = models.IntegerField(null=True, blank=True)  # Can be null for advanced questions
    second_number = models.IntegerField(null=True, blank=True)  # Can be null for advanced questions
    question_text = models.TextField(null=True, blank=True)  # For advanced questions like expressions
    answer = models.FloatField()  # Using float to accommodate division results
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_operation_display()} - {self.first_number} {self.get_operation_symbol()} {self.second_number}"

    def get_operation_symbol(self):
        symbols = {
            'addition': '+',
            'subtraction': '-',
            'multiplication': '×',
            'division': '÷',
        }
        return symbols.get(self.operation, '')

    def get_question_display(self):
        """Get the display text for the question"""
        if self.question_text:
            return self.question_text
        elif self.first_number is not None and self.second_number is not None:
            return f"{self.first_number} {self.get_operation_symbol()} {self.second_number}"
        else:
            return "سؤال متقدم"

    def check_answer(self, user_answer):
        try:
            user_answer_float = float(user_answer)
            # For division and advanced operations, allow small floating point differences
            if self.operation in ['division', 'fractions', 'algebra', 'geometry', 'trigonometry', 'word_problems']:
                return abs(user_answer_float - self.answer) < 0.01  # Allow 0.01 difference
            else:
                return abs(user_answer_float - self.answer) < 0.001  # Very small difference for basic operations
        except (ValueError, TypeError):
            return False

    @classmethod
    def get_stage_from_difficulty(cls, difficulty):
        """Get stage number from difficulty level"""
        if 1 <= difficulty <= 6:
            return 1
        elif 7 <= difficulty <= 9:
            return 2
        return 1

    @classmethod
    def get_time_per_question(cls, difficulty):
        """Get time per question in seconds based on difficulty level"""
        if 1 <= difficulty <= 4:
            return 15  # 15 seconds for levels 1-4
        elif 5 <= difficulty <= 9:
            return 10  # 10 seconds for levels 5-9
        return 15  # default

    @classmethod
    def get_question_distribution(cls, difficulty):
        """Get question distribution for each difficulty level"""
        distributions = {
            # المرحلة الأولى
            1: {'addition': 8, 'subtraction': 7},  # المستوى الأول
            2: {'addition': 5, 'subtraction': 5, 'multiplication': 5},  # المستوى الثاني
            3: {'addition': 4, 'subtraction': 4, 'multiplication': 5, 'division': 2},  # المستوى الثالث
            4: {'addition': 4, 'subtraction': 4, 'multiplication': 5, 'division': 2},  # المستوى الرابع
            5: {'addition': 4, 'subtraction': 4, 'multiplication': 5, 'division': 2},  # المستوى الخامس
            6: {'addition': 4, 'subtraction': 4, 'multiplication': 4, 'division': 3},  # المستوى السادس

            # المرحلة الثانية
            7: {'mixed_operations': 10, 'word_problems': 5},  # المستوى الأول - المرحلة الثانية
            8: {'fractions': 5, 'mixed_operations': 4, 'algebra': 3, 'word_problems': 3},  # المستوى الثاني - المرحلة الثانية
            9: {'algebra': 4, 'geometry': 6, 'trigonometry': 3, 'word_problems': 2},  # المستوى الثالث - المرحلة الثانية
        }
        return distributions.get(difficulty, distributions[1])

class Competition(models.Model):
    """
    Model for tracking a user's competition session.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competitions', null=True, blank=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='competitions', null=True, blank=True)
    difficulty = models.IntegerField(choices=MathQuestion.DIFFICULTY_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(9)])
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.get_difficulty_display()} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
        elif self.participant:
            return f"{self.participant.name} - {self.get_difficulty_display()} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
        else:
            return f"مسابقة بدون مشارك - {self.get_difficulty_display()} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    @property
    def duration(self):
        if not self.end_time:
            return None
        return (self.end_time - self.start_time).total_seconds()

    @property
    def total_score(self):
        return self.responses.filter(is_correct=True).count() * 3  # 3 points per correct answer

class UserResponse(models.Model):
    """
    Model for tracking user responses to questions.
    """
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(MathQuestion, on_delete=models.CASCADE, related_name='responses')
    user_answer = models.FloatField(null=True, blank=True)  # Null if the user didn't answer
    is_correct = models.BooleanField(default=False)
    response_time = models.FloatField(help_text="Time taken to answer in seconds", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "صحيحة" if self.is_correct else "خاطئة"
        if self.competition.user:
            return f"{self.competition.user.username} - {self.question} - {status}"
        elif self.competition.participant:
            return f"{self.competition.participant.name} - {self.question} - {status}"
        else:
            return f"مسابقة بدون مشارك - {self.question} - {status}"

class CompetitionResult(models.Model):
    """
    Model for storing the final results of a competition.
    """
    competition = models.OneToOneField(Competition, on_delete=models.CASCADE, related_name='result')
    total_score = models.IntegerField(default=0)
    addition_correct = models.IntegerField(default=0)
    subtraction_correct = models.IntegerField(default=0)
    multiplication_correct = models.IntegerField(default=0)
    division_correct = models.IntegerField(default=0)
    # إضافة العمليات الجديدة
    mixed_operations_correct = models.IntegerField(default=0)
    fractions_correct = models.IntegerField(default=0)
    algebra_correct = models.IntegerField(default=0)
    geometry_correct = models.IntegerField(default=0)
    trigonometry_correct = models.IntegerField(default=0)
    word_problems_correct = models.IntegerField(default=0)

    addition_total = models.IntegerField(default=0)
    subtraction_total = models.IntegerField(default=0)
    multiplication_total = models.IntegerField(default=0)
    division_total = models.IntegerField(default=0)
    # إضافة المجاميع للعمليات الجديدة
    mixed_operations_total = models.IntegerField(default=0)
    fractions_total = models.IntegerField(default=0)
    algebra_total = models.IntegerField(default=0)
    geometry_total = models.IntegerField(default=0)
    trigonometry_total = models.IntegerField(default=0)
    word_problems_total = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.competition.user:
            return f"{self.competition.user.username} - {self.total_score} نقاط"
        elif self.competition.participant:
            return f"{self.competition.participant.name} - {self.total_score} نقاط"
        else:
            return f"مسابقة بدون مشارك - {self.total_score} نقاط"

    @property
    def addition_percentage(self):
        if self.addition_total == 0:
            return 0
        return (self.addition_correct / self.addition_total) * 100

    @property
    def subtraction_percentage(self):
        if self.subtraction_total == 0:
            return 0
        return (self.subtraction_correct / self.subtraction_total) * 100

    @property
    def multiplication_percentage(self):
        if self.multiplication_total == 0:
            return 0
        return (self.multiplication_correct / self.multiplication_total) * 100

    @property
    def division_percentage(self):
        if self.division_total == 0:
            return 0
        return (self.division_correct / self.division_total) * 100

    @property
    def mixed_operations_percentage(self):
        if self.mixed_operations_total == 0:
            return 0
        return (self.mixed_operations_correct / self.mixed_operations_total) * 100

    @property
    def fractions_percentage(self):
        if self.fractions_total == 0:
            return 0
        return (self.fractions_correct / self.fractions_total) * 100

    @property
    def algebra_percentage(self):
        if self.algebra_total == 0:
            return 0
        return (self.algebra_correct / self.algebra_total) * 100

    @property
    def geometry_percentage(self):
        if self.geometry_total == 0:
            return 0
        return (self.geometry_correct / self.geometry_total) * 100

    @property
    def trigonometry_percentage(self):
        if self.trigonometry_total == 0:
            return 0
        return (self.trigonometry_correct / self.trigonometry_total) * 100

    @property
    def word_problems_percentage(self):
        if self.word_problems_total == 0:
            return 0
        return (self.word_problems_correct / self.word_problems_total) * 100

    # دوال حساب النسب المختلفة للنتيجة الإجمالية
    @property
    def percentage_100(self):
        """حساب النسبة المئوية من 100"""
        if self.total_score is None:
            return 0
        return round((self.total_score / 45) * 100, 1)

    @property
    def percentage_10(self):
        """حساب النسبة من 10"""
        if self.total_score is None:
            return 0
        return round((self.total_score / 45) * 10, 1)

    @property
    def percentage_20(self):
        """حساب النسبة من 20"""
        if self.total_score is None:
            return 0
        return round((self.total_score / 45) * 20, 1)

    @property
    def score_color_class(self):
        """تحديد لون النتيجة حسب النسبة المئوية"""
        percentage = self.percentage_100
        if percentage >= 75:
            return 'text-success'  # أخضر
        elif percentage >= 50:
            return 'text-warning'  # أصفر
        else:
            return 'text-danger'   # أحمر

    @property
    def score_badge_class(self):
        """تحديد نوع الشارة حسب النسبة المئوية"""
        percentage = self.percentage_100
        if percentage >= 75:
            return 'bg-success'  # أخضر
        elif percentage >= 50:
            return 'bg-warning'  # أصفر
        else:
            return 'bg-danger'   # أحمر

    @property
    def performance_level(self):
        """تحديد مستوى الأداء"""
        percentage = self.percentage_100
        if percentage >= 90:
            return 'ممتاز'
        elif percentage >= 75:
            return 'جيد جداً'
        elif percentage >= 60:
            return 'جيد'
        elif percentage >= 50:
            return 'مقبول'
        else:
            return 'ضعيف'

    @property
    def performance_emoji(self):
        """رمز تعبيري للأداء"""
        percentage = self.percentage_100
        if percentage >= 90:
            return '🌟'  # ممتاز
        elif percentage >= 75:
            return '😊'  # جيد جداً
        elif percentage >= 60:
            return '🙂'  # جيد
        elif percentage >= 50:
            return '😐'  # مقبول
        else:
            return '😞'  # ضعيف

    def get_formatted_score_display(self):
        """عرض النتيجة بالصيغة الموحدة"""
        return {
            'original': f"{self.total_score} / 45",
            'percentage_100': f"{self.percentage_100}%",
            'percentage_10': f"{self.percentage_10} / 10",
            'percentage_20': f"{self.percentage_20} / 20",
            'color_class': self.score_color_class,
            'badge_class': self.score_badge_class,
            'performance_level': self.performance_level,
            'performance_emoji': self.performance_emoji
        }


# ==================== Student Models ====================

class StudentSession(models.Model):
    """نموذج لجلسات التلاميذ الذين يدخلون برمز"""

    GRADE_CHOICES = [
        (1, 'المستوى الأول ابتدائي'),
        (2, 'المستوى الثاني ابتدائي'),
        (3, 'المستوى الثالث ابتدائي'),
        (4, 'المستوى الرابع ابتدائي'),
        (5, 'المستوى الخامس ابتدائي'),
        (6, 'المستوى السادس ابتدائي'),
        (7, 'المستوى الأول إعدادي'),
        (8, 'المستوى الثاني إعدادي'),
        (9, 'المستوى الثالث إعدادي'),
    ]

    DIFFICULTY_CHOICES = [
        (1, 'المستوى الأول - المرحلة الأولى'),
        (2, 'المستوى الثاني - المرحلة الأولى'),
        (3, 'المستوى الثالث - المرحلة الأولى'),
        (4, 'المستوى الرابع - المرحلة الأولى'),
        (5, 'المستوى الخامس - المرحلة الأولى'),
        (6, 'المستوى السادس - المرحلة الأولى'),
        (7, 'الجمع والطرح - متدرج'),
        (8, 'الضرب - متدرج'),
        (9, 'القسمة - متدرج'),
    ]

    # معلومات التلميذ
    student_name = models.CharField(max_length=100, verbose_name="اسم التلميذ")
    grade = models.IntegerField(choices=GRADE_CHOICES, verbose_name="المستوى الدراسي")
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, verbose_name="مستوى الصعوبة")

    # معلومات الجلسة
    session_code = models.CharField(max_length=20, default="ben25", verbose_name="رمز الدخول")
    start_time = models.DateTimeField(default=timezone.now, verbose_name="وقت البداية")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="وقت الانتهاء")
    is_completed = models.BooleanField(default=False, verbose_name="مكتملة")

    # النتائج
    total_questions = models.IntegerField(default=0, verbose_name="إجمالي الأسئلة")
    correct_answers = models.IntegerField(default=0, verbose_name="الإجابات الصحيحة")
    total_score = models.IntegerField(default=0, verbose_name="النقاط الإجمالية")

    # تفاصيل الأداء
    addition_correct = models.IntegerField(default=0, verbose_name="الجمع الصحيح")
    addition_total = models.IntegerField(default=0, verbose_name="إجمالي الجمع")
    subtraction_correct = models.IntegerField(default=0, verbose_name="الطرح الصحيح")
    subtraction_total = models.IntegerField(default=0, verbose_name="إجمالي الطرح")
    multiplication_correct = models.IntegerField(default=0, verbose_name="الضرب الصحيح")
    multiplication_total = models.IntegerField(default=0, verbose_name="إجمالي الضرب")
    division_correct = models.IntegerField(default=0, verbose_name="القسمة الصحيحة")
    division_total = models.IntegerField(default=0, verbose_name="إجمالي القسمة")

    # معلومات إضافية
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="عنوان IP")
    user_agent = models.TextField(null=True, blank=True, verbose_name="معلومات المتصفح")

    class Meta:
        verbose_name = "جلسة تلميذ"
        verbose_name_plural = "جلسات التلاميذ"
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.student_name} - {self.get_grade_display()} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    @property
    def duration_minutes(self):
        """حساب مدة الجلسة بالدقائق"""
        if self.end_time:
            duration = self.end_time - self.start_time
            return round(duration.total_seconds() / 60, 1)
        return 0

    @property
    def success_rate(self):
        """حساب معدل النجاح"""
        if self.total_questions > 0:
            return round((self.correct_answers / self.total_questions) * 100, 1)
        return 0

    @property
    def addition_percentage(self):
        """نسبة نجاح الجمع"""
        if self.addition_total > 0:
            return round((self.addition_correct / self.addition_total) * 100, 1)
        return 0

    @property
    def subtraction_percentage(self):
        """نسبة نجاح الطرح"""
        if self.subtraction_total > 0:
            return round((self.subtraction_correct / self.subtraction_total) * 100, 1)
        return 0

    @property
    def multiplication_percentage(self):
        """نسبة نجاح الضرب"""
        if self.multiplication_total > 0:
            return round((self.multiplication_correct / self.multiplication_total) * 100, 1)
        return 0

    @property
    def division_percentage(self):
        """نسبة نجاح القسمة"""
        if self.division_total > 0:
            return round((self.division_correct / self.division_total) * 100, 1)
        return 0

    @property
    def strengths(self):
        """نقاط القوة"""
        strengths = []
        operations = [
            ('الجمع', self.addition_percentage),
            ('الطرح', self.subtraction_percentage),
            ('الضرب', self.multiplication_percentage),
            ('القسمة', self.division_percentage),
        ]

        for operation, percentage in operations:
            if percentage >= 80:
                strengths.append(operation)

        return strengths

    @property
    def weaknesses(self):
        """نقاط الضعف"""
        weaknesses = []
        operations = [
            ('الجمع', self.addition_percentage),
            ('الطرح', self.subtraction_percentage),
            ('الضرب', self.multiplication_percentage),
            ('القسمة', self.division_percentage),
        ]

        for operation, percentage in operations:
            if percentage < 60 and percentage > 0:
                weaknesses.append(operation)

        return weaknesses


class StudentResponse(models.Model):
    """نموذج لإجابات التلاميذ"""

    session = models.ForeignKey(StudentSession, on_delete=models.CASCADE, related_name='responses', verbose_name="الجلسة")

    # السؤال
    operation = models.CharField(max_length=20, verbose_name="نوع العملية")
    first_number = models.IntegerField(verbose_name="الرقم الأول")
    second_number = models.IntegerField(verbose_name="الرقم الثاني")
    correct_answer = models.IntegerField(verbose_name="الإجابة الصحيحة")

    # الإجابة
    student_answer = models.IntegerField(null=True, blank=True, verbose_name="إجابة التلميذ")
    is_correct = models.BooleanField(default=False, verbose_name="صحيحة")
    response_time = models.FloatField(null=True, blank=True, verbose_name="وقت الإجابة (ثانية)")

    # التوقيت
    created_at = models.DateTimeField(default=timezone.now, verbose_name="وقت الإنشاء")

    class Meta:
        verbose_name = "إجابة تلميذ"
        verbose_name_plural = "إجابات التلاميذ"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.session.student_name} - {self.first_number} {self.operation} {self.second_number}"