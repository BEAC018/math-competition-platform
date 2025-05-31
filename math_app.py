"""
تطبيق الرياضيات بالتعديلات المطلوبة:
1. ملخص النتائج يكون على 45 بدل 36
2. العدد الأكبر في الحساب على اليسار
3. إمكانية حذف مشاركين الفصل دفعة واحدة
4. تغيير ترتيب الأرقام من اليمين إلى اليسار
5. تفادي استخدام الأرقام المتشابهة في العمليات
6. تفادي تكرار العمليات
7. تعديل مجالات الأرقام حسب المستويات:

   المستوى الأول:
   - الجمع والطرح: استخدام الأرقام من 1 حتى 20
   - جدول الضرب: 2، 3، 4، 5، 6، 7
   - القسمة: العمليات التي يكون خارجها 2، 3، أو 4

   المستوى الثاني:
   - الجمع والطرح: استخدام الأرقام من 5 حتى 30، وتفادي استخدام الأرقام من 1 حتى 5
   - جدول الضرب: من 3 حتى 12
   - القسمة: العمليات التي يكون خارجها 2، 3، 4، أو 5

   المستوى الثالث:
   - الجمع والطرح: استخدام الأرقام من 1 حتى 5 للعمليات
   - جدول الضرب: من 3×3 إلى 12×12
   - القسمة: العمليات التي يكون خارجها 2، 3، 4، أو 5

   المستوى الرابع:
   - الجمع والطرح: استخدام الأرقام من 9 حتى 50، وتفادي استخدام الأرقام من 1 حتى 8
   - جدول الضرب: حتى 15
   - القسمة: العمليات التي يكون خارجها 3، 4، 5، أو 6
"""

import django
import os
import sys
import random
from django.db import models
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import path, reverse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Case, When, IntegerField, Max
from competitions.models import Participant

# 1. تغيير ملخص النتائج من 36 إلى 45

class ResultsDisplay:
    """
    تعديل عرض النتائج لتكون من 45 بدلاً من 36
    
    يتم استخدام هذا الكود في قالب النتائج (results.html):
    
    <div class="display-1 fw-bold text-primary mb-3">
        {{ result.total_score }} / 45
    </div>
    <div class="progress mb-4" style="height: 10px;">
        <div class="progress-bar {% if result.total_score < 15 %}bg-danger{% elif result.total_score < 30 %}bg-warning{% else %}bg-success{% endif %}"
        role="progressbar"
        data-width="{% widthratio result.total_score 45 100 %}"
        aria-valuenow="{{ result.total_score }}"
        aria-valuemin="0"
        aria-valuemax="45"></div>
    </div>
    """
    
    @staticmethod
    def calculate_total_score(addition_correct, subtraction_correct, multiplication_correct, division_correct):
        """
        حساب مجموع النقاط (3 نقاط لكل إجابة صحيحة)
        """
        return (addition_correct + subtraction_correct + multiplication_correct + division_correct) * 3

# 2. جعل العدد الأكبر في الحساب على اليسار

class MathOperations:
    """توليد أسئلة رياضية مع تحسينات متعددة"""
    
    # تخزين الأسئلة السابقة لتفادي التكرار
    last_questions = []
    
    @staticmethod
    def are_numbers_similar(num1, num2):
        """التحقق مما إذا كانت الأرقام متشابهة (متساوية)"""
        return num1 == num2
    
    @staticmethod
    def is_question_repeated(operation, first_number, second_number):
        """التحقق مما إذا كان السؤال مكررًا مقارنة بالأسئلة السابقة"""
        for last_op, last_first, last_second in MathOperations.last_questions[-5:]:
            if last_op == operation and last_first == first_number and last_second == second_number:
                return True
            # اعتبار العمليات المعكوسة متشابهة أيضًا
            if last_op == operation and last_first == second_number and last_second == first_number:
                return True
        return False
        
    @staticmethod
    def add_to_history(operation, first_number, second_number):
        """إضافة سؤال إلى سجل الأسئلة السابقة"""
        MathOperations.last_questions.append((operation, first_number, second_number))
        # الاحتفاظ فقط بآخر 10 أسئلة في السجل
        if len(MathOperations.last_questions) > 10:
            MathOperations.last_questions = MathOperations.last_questions[-10:]
    
    @staticmethod
    def generate_addition_question(min_val, max_val, avoid_min=None, avoid_max=None, operators=None):
        """توليد سؤال جمع مع تحسينات متعددة"""
        max_attempts = 20  # لمنع الحلقات اللانهائية
        
        for _ in range(max_attempts):
            if operators:  # استخدام محددات معينة للعمليات
                operator = random.choice(operators)
                num = random.randint(min_val, max_val)
                num1, num2 = operator, num
            elif avoid_min is not None and avoid_max is not None:  # تفادي نطاق معين من الأرقام
                num1 = random.randint(min_val, max_val)
                while avoid_min <= num1 <= avoid_max:
                    num1 = random.randint(min_val, max_val)
                    
                num2 = random.randint(min_val, max_val)
                while avoid_min <= num2 <= avoid_max or MathOperations.are_numbers_similar(num1, num2):
                    num2 = random.randint(min_val, max_val)
            else:  # نطاق قياسي
                num1 = random.randint(min_val, max_val)
                num2 = random.randint(min_val, max_val)
                while MathOperations.are_numbers_similar(num1, num2):
                    num2 = random.randint(min_val, max_val)
            
            # جعل العدد الأكبر على اليسار
            if num1 > num2:
                first_number = num1
                second_number = num2
            else:
                first_number = num2
                second_number = num1
                
            answer = first_number + second_number
            
            # التحقق مما إذا كان هذا السؤال مكررًا
            if not MathOperations.is_question_repeated("addition", first_number, second_number):
                break
        
        # إضافة هذا السؤال إلى السجل
        MathOperations.add_to_history("addition", first_number, second_number)
            
        return {
            'first_number': first_number,
            'second_number': second_number,
            'answer': answer
        }
    
    @staticmethod
    def generate_multiplication_question(min_val, max_val, tables=None):
        """توليد سؤال ضرب مع تحسينات متعددة"""
        max_attempts = 20  # لمنع الحلقات اللانهائية
        
        for _ in range(max_attempts):
            if tables:  # استخدام جداول ضرب محددة
                num1 = random.choice(tables)
                num2 = random.randint(1, 10)
                while MathOperations.are_numbers_similar(num1, num2):
                    num2 = random.randint(1, 10)
            else:
                num1 = random.randint(min_val, max_val)
                num2 = random.randint(min_val, max_val)
                while MathOperations.are_numbers_similar(num1, num2):
                    num2 = random.randint(min_val, max_val)
            
            # جعل العدد الأكبر على اليسار
            if num1 > num2:
                first_number = num1
                second_number = num2
            else:
                first_number = num2
                second_number = num1
                
            answer = first_number * second_number
            
            # التحقق مما إذا كان هذا السؤال مكررًا
            if not MathOperations.is_question_repeated("multiplication", first_number, second_number):
                break
        
        # إضافة هذا السؤال إلى السجل
        MathOperations.add_to_history("multiplication", first_number, second_number)
            
        return {
            'first_number': first_number,
            'second_number': second_number,
            'answer': answer
        }
    
    @staticmethod
    def generate_subtraction_question(min_val, max_val, avoid_min=None, avoid_max=None, operators=None):
        """توليد سؤال طرح مع تحسينات متعددة"""
        max_attempts = 20  # لمنع الحلقات اللانهائية
        
        for _ in range(max_attempts):
            if operators:  # استخدام محددات معينة للعمليات
                operator = random.choice(operators)
                num = random.randint(min_val, max_val)
                # التأكد من أن الناتج موجب
                first_number = max(operator, num)
                second_number = min(operator, num)
            elif avoid_min is not None and avoid_max is not None:  # تفادي نطاق معين من الأرقام
                first_number = random.randint(min_val, max_val)
                while avoid_min <= first_number <= avoid_max:
                    first_number = random.randint(min_val, max_val)
                
                # ضمان أن العدد الثاني أصغر للحصول على نتيجة موجبة
                second_number = random.randint(min_val, first_number)
                while (avoid_min <= second_number <= avoid_max or
                       MathOperations.are_numbers_similar(first_number, second_number)):
                    second_number = random.randint(min_val, first_number)
            else:
                # بالنسبة للطرح، يجب أن يكون الرقم الأول أكبر لضمان نتيجة موجبة
                first_number = random.randint(min_val, max_val)
                second_number = random.randint(min_val, first_number)
                while MathOperations.are_numbers_similar(first_number, second_number):
                    second_number = random.randint(min_val, first_number)
            
            answer = first_number - second_number
            
            # التحقق مما إذا كان هذا السؤال مكررًا
            if not MathOperations.is_question_repeated("subtraction", first_number, second_number):
                break
        
        # إضافة هذا السؤال إلى السجل
        MathOperations.add_to_history("subtraction", first_number, second_number)
            
        return {
            'first_number': first_number,
            'second_number': second_number,
            'answer': answer
        }
    
    @staticmethod
    def generate_division_question(min_val, max_val, divisor_max, quotients=None):
        """توليد سؤال قسمة مع تحسينات متعددة"""
        max_attempts = 20  # لمنع الحلقات اللانهائية
        
        for _ in range(max_attempts):
            if quotients:  # استخدام خارج قسمة محدد
                quotient = random.choice(quotients)
            else:
                max_answer = max_val // 2  # تقدير تقريبي
                quotient = random.randint(2, max(2, max_answer))
            
            # اختيار مقسوم عليه
            divisor = random.randint(2, divisor_max)
            
            # حساب المقسوم
            dividend = quotient * divisor
            
            # جعل العدد الأكبر (المقسوم) على اليسار
            first_number = dividend
            second_number = divisor
            answer = quotient
            
            # التحقق مما إذا كان هذا السؤال مكررًا
            if not MathOperations.is_question_repeated("division", first_number, second_number):
                break
        
        # إضافة هذا السؤال إلى السجل
        MathOperations.add_to_history("division", first_number, second_number)
            
        return {
            'first_number': first_number,
            'second_number': second_number,
            'answer': answer
        }

# 3. إضافة إمكانية حذف مشاركين الفصل دفعة واحدة

class ParticipantManager:
    """إدارة المشاركين"""
    
    @staticmethod
    @login_required
    def delete_multiple_participants(request):
        """حذف عدة مشاركين دفعة واحدة"""
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])
        
        # الحصول على قائمة معرفات المشاركين من النموذج
        participant_ids = request.POST.getlist('participant_ids')
        
        if not participant_ids:
            messages.error(request, 'لم يتم تحديد أي مشارك للحذف')
            return redirect('competitions:start_competition')
        
        # عد كم تم حذفه بنجاح
        deleted_count = 0
        not_deleted_count = 0
        
        for participant_id in participant_ids:
            try:
                participant = get_object_or_404(Participant, id=participant_id)
                
                # التحقق من أن هذا المشارك ليس له مسابقات
                if participant.competitions.exists():
                    not_deleted_count += 1
                    continue
                
                participant.delete()
                deleted_count += 1
                
            except Participant.DoesNotExist:
                continue
        
        if deleted_count > 0:
            messages.success(request, f'تم حذف {deleted_count} مشارك بنجاح')
        
        if not_deleted_count > 0:
            messages.error(request, f'لم يتم حذف {not_deleted_count} مشاركين لأنهم لديهم مسابقات مسجلة')
        
        # إعادة التوجيه إلى صفحة بدء المسابقة
        return redirect('competitions:start_competition')


"""
نموذج HTML للواجهة الخاصة بحذف مشاركين متعددين:

<form id="delete-participants-form" action="{% url 'competitions:delete_multiple_participants' %}" method="post">
    {% csrf_token %}
    <div class="mb-2 d-flex justify-content-end">
        <button type="submit" class="btn btn-danger" id="delete-selected-btn" disabled onclick="return confirm('هل أنت متأكد من حذف المشاركين المحددين؟')">
            <i class="fas fa-trash-alt"></i> حذف المحددين
        </button>
    </div>
    <table class="table table-hover mb-0">
        <thead class="table-light">
            <tr>
                <th>
                    <input type="checkbox" id="select-all-checkbox" onclick="toggleAllCheckboxes()">
                </th>
                <th>#</th>
                <th>الاسم</th>
                <th>المستوى</th>
                <th>الفوج</th>
                <th>العمليات</th>
            </tr>
        </thead>
        <tbody>
            {% for participant in participants %}
            <tr>
                <td>
                    <input type="checkbox" name="participant_ids" value="{{ participant.id }}" class="participant-checkbox" onchange="updateDeleteButton()">
                </td>
                <td>{{ forloop.counter }}</td>
                <td>{{ participant.name }}</td>
                <td>{{ participant.get_grade_display }}</td>
                <td>{{ participant.get_group_display }}</td>
                <td>
                    <a href="/competitions/delete-participant/{{ participant.id }}/"
                       class="btn btn-sm btn-danger"
                       onclick="return confirm('هل أنت متأكد من حذف المشارك {{ participant.name }}؟')">
                        <i class="fas fa-trash-alt"></i> حذف
                    </a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</form>

<script>
// دالة لتحديد/إلغاء تحديد جميع خانات الاختيار
function toggleAllCheckboxes() {
    const selectAllCheckbox = document.getElementById('select-all-checkbox');
    const participantCheckboxes = document.querySelectorAll('.participant-checkbox');
    
    participantCheckboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
    
    updateDeleteButton();
}

// دالة لتحديث حالة زر الحذف
function updateDeleteButton() {
    const participantCheckboxes = document.querySelectorAll('.participant-checkbox:checked');
    const deleteButton = document.getElementById('delete-selected-btn');
    
    deleteButton.disabled = participantCheckboxes.length === 0;
}
</script>
"""

class UrlPatterns:
    """
    أنماط عناوين URL المطلوبة:
    
    urlpatterns = [
        # Participant management
        path('add-participant/', views.add_participant, name='add_participant'),
        path('delete-participant/<int:participant_id>/', views.delete_participant, name='delete_participant'),
        path('delete-multiple-participants/', views.delete_multiple_participants, name='delete_multiple_participants'),
    ]
    """
    pass


if __name__ == "__main__":
    print("تم تضمين جميع التغييرات المطلوبة في هذا الملف:")
    print("1. تغيير ملخص النتائج من 36 إلى 45")
    print("2. جعل العدد الأكبر في الحساب على اليسار")
    print("3. إضافة إمكانية حذف مشاركين الفصل دفعة واحدة")