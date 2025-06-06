from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Question, Competition, Answer
import random


def competition_start(request):
    """بداية المسابقة"""
    # التحقق من وجود جلسة طالب
    if 'student_name' not in request.session:
        return redirect('student_login')

    student_name = request.session.get('student_name')
    grade_level = request.session.get('grade_level')
    difficulty_level = request.session.get('difficulty_level', 'medium')

    # إنشاء مسابقة جديدة
    competition = Competition.objects.create(
        student_name=student_name,
        grade_level=grade_level,
        total_questions=10
    )

    # حفظ معرف المسابقة في الجلسة
    request.session['competition_id'] = competition.id

    return render(request, 'competitions/start.html', {
        'student_name': student_name,
        'grade_level': grade_level,
        'difficulty_level': difficulty_level,
        'competition': competition
    })


def get_question(request):
    """الحصول على سؤال جديد"""
    if 'competition_id' not in request.session:
        return redirect('student_login')
    
    competition = get_object_or_404(Competition, id=request.session['competition_id'])
    
    # التحقق من عدد الأسئلة المجابة
    answered_count = Answer.objects.filter(competition=competition).count()
    
    if answered_count >= competition.total_questions:
        # انتهاء المسابقة
        competition.is_completed = True
        competition.end_time = timezone.now()
        competition.calculate_score()
        competition.save()
        return redirect('competition_results')
    
    # إنشاء سؤال رياضي عشوائي
    difficulty_level = request.session.get('difficulty_level', 'medium')
    question = generate_random_question(competition.grade_level, difficulty_level)
    
    context = {
        'question': question,
        'question_number': answered_count + 1,
        'total_questions': competition.total_questions,
        'student_name': competition.student_name
    }
    
    return render(request, 'competitions/question.html', context)


def submit_answer(request):
    """إرسال الإجابة"""
    if request.method == 'POST' and 'competition_id' in request.session:
        competition = get_object_or_404(Competition, id=request.session['competition_id'])
        
        question_text = request.POST.get('question_text')
        correct_answer = int(request.POST.get('correct_answer'))
        student_answer = int(request.POST.get('student_answer', 0))
        
        # إنشاء سؤال مؤقت (في التطبيق الحقيقي، يجب حفظ الأسئلة في قاعدة البيانات)
        question = Question(
            question_text=question_text,
            correct_answer=correct_answer,
            operation_type='mixed',
            difficulty='medium',
            grade_level=competition.grade_level
        )
        question.save()
        
        # حفظ الإجابة
        is_correct = student_answer == correct_answer
        Answer.objects.create(
            competition=competition,
            question=question,
            student_answer=student_answer,
            is_correct=is_correct
        )
        
        # تحديث عدد الإجابات الصحيحة
        if is_correct:
            competition.correct_answers += 1
            competition.save()
        
        return JsonResponse({
            'correct': is_correct,
            'correct_answer': correct_answer
        })
    
    return JsonResponse({'error': 'خطأ في الإرسال'})


def competition_results(request):
    """نتائج المسابقة"""
    if 'competition_id' not in request.session:
        return redirect('student_login')
    
    competition = get_object_or_404(Competition, id=request.session['competition_id'])
    answers = Answer.objects.filter(competition=competition)
    
    context = {
        'competition': competition,
        'answers': answers,
        'percentage': competition.score
    }
    
    return render(request, 'competitions/results.html', context)


def generate_random_question(grade_level, difficulty_level='medium'):
    """إنشاء سؤال رياضي عشوائي حسب مستوى الصعوبة"""
    operations = ['+', '-', '*', '/']
    operation = random.choice(operations)

    # تحديد نطاق الأرقام حسب مستوى الصعوبة
    if difficulty_level == 'easy':
        # سهل: أرقام صغيرة
        add_range = (1, 20)
        sub_range = (5, 30)
        mul_range = (1, 5)
        div_range = (2, 5)
    elif difficulty_level == 'hard':
        # صعب: أرقام كبيرة
        add_range = (50, 200)
        sub_range = (100, 500)
        mul_range = (10, 25)
        div_range = (5, 20)
    else:
        # متوسط: أرقام متوسطة
        add_range = (10, 100)
        sub_range = (20, 150)
        mul_range = (2, 15)
        div_range = (2, 12)

    if operation == '+':
        a = random.randint(*add_range)
        b = random.randint(*add_range)
        question = f"{a} + {b}"
        answer = a + b
    elif operation == '-':
        a = random.randint(*sub_range)
        b = random.randint(1, a)
        question = f"{a} - {b}"
        answer = a - b
    elif operation == '*':
        a = random.randint(*mul_range)
        b = random.randint(*mul_range)
        question = f"{a} × {b}"
        answer = a * b
    else:  # division
        b = random.randint(*div_range)
        answer = random.randint(1, div_range[1])
        a = b * answer
        question = f"{a} ÷ {b}"

    return {
        'text': question,
        'answer': answer,
        'difficulty': difficulty_level
    }
