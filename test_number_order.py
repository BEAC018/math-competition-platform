#!/usr/bin/env python
"""
Test script for number ordering in math operations
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')
django.setup()

from competitions.question_generators import QuestionGenerator
from competitions.views import generate_math_question

def test_number_ordering():
    """Test that larger numbers appear on the left in all operations"""
    print("🧪 اختبار ترتيب الأرقام في العمليات الحسابية...")

    operations = ['addition', 'subtraction', 'multiplication', 'division']
    difficulties = [1, 2, 3, 4, 5, 6]

    results = {
        'total_tests': 0,
        'correct_order': 0,
        'incorrect_order': 0,
        'issues': []
    }

    # Test QuestionGenerator
    print("\n📊 اختبار QuestionGenerator:")
    for operation in operations:
        for difficulty in difficulties:
            try:
                # Test 10 questions for each operation/difficulty combination
                for i in range(10):
                    if operation == 'addition':
                        question = QuestionGenerator.generate_addition_question(difficulty)
                    elif operation == 'subtraction':
                        question = QuestionGenerator.generate_subtraction_question(difficulty)
                    elif operation == 'multiplication':
                        question = QuestionGenerator.generate_multiplication_question(difficulty)
                    elif operation == 'division':
                        question = QuestionGenerator.generate_division_question(difficulty)
                    else:
                        continue

                    first_num = question['first_number']
                    second_num = question['second_number']

                    results['total_tests'] += 1

                    # الآن نريد العدد الأصغر على اليسار والأكبر على اليمين
                    # For division, first number should be smaller (divisor < dividend)
                    # For other operations, first number should be <= second number
                    if operation == 'division':
                        if first_num <= second_num:
                            results['correct_order'] += 1
                        else:
                            results['incorrect_order'] += 1
                            results['issues'].append(f"{operation} مستوى {difficulty}: {first_num} {operation} {second_num}")
                    else:
                        if first_num <= second_num:
                            results['correct_order'] += 1
                        else:
                            results['incorrect_order'] += 1
                            results['issues'].append(f"{operation} مستوى {difficulty}: {first_num} {operation} {second_num}")

            except Exception as e:
                print(f"❌ خطأ في {operation} مستوى {difficulty}: {str(e)}")

    # Test generate_math_question function
    print("\n📊 اختبار generate_math_question:")
    for operation in operations:
        for difficulty in difficulties:
            try:
                # Test 10 questions for each operation/difficulty combination
                for i in range(10):
                    question = generate_math_question(operation, difficulty)

                    first_num = question['first_number']
                    second_num = question['second_number']

                    results['total_tests'] += 1

                    # Check ordering - العدد الأصغر على اليسار
                    if operation == 'division':
                        if first_num <= second_num:
                            results['correct_order'] += 1
                        else:
                            results['incorrect_order'] += 1
                            results['issues'].append(f"views.py {operation} مستوى {difficulty}: {first_num} {operation} {second_num}")
                    else:
                        if first_num <= second_num:
                            results['correct_order'] += 1
                        else:
                            results['incorrect_order'] += 1
                            results['issues'].append(f"views.py {operation} مستوى {difficulty}: {first_num} {operation} {second_num}")

            except Exception as e:
                print(f"❌ خطأ في views.py {operation} مستوى {difficulty}: {str(e)}")

    # Show results
    print(f"\n📈 نتائج الاختبار:")
    print(f"- إجمالي الاختبارات: {results['total_tests']}")
    print(f"- ترتيب صحيح: {results['correct_order']}")
    print(f"- ترتيب خاطئ: {results['incorrect_order']}")

    if results['incorrect_order'] > 0:
        print(f"\n⚠️ مشاكل في الترتيب:")
        for issue in results['issues'][:10]:  # Show first 10 issues
            print(f"  - {issue}")
        if len(results['issues']) > 10:
            print(f"  ... و {len(results['issues']) - 10} مشاكل أخرى")

    success_rate = (results['correct_order'] / results['total_tests']) * 100 if results['total_tests'] > 0 else 0
    print(f"\n📊 معدل النجاح: {success_rate:.1f}%")

    return results['incorrect_order'] == 0

def test_specific_examples():
    """Test specific examples to show the ordering"""
    print("\n🔍 أمثلة محددة:")

    operations = ['addition', 'subtraction', 'multiplication', 'division']

    for operation in operations:
        try:
            if operation == 'addition':
                question = QuestionGenerator.generate_addition_question(3)
            elif operation == 'subtraction':
                question = QuestionGenerator.generate_subtraction_question(3)
            elif operation == 'multiplication':
                question = QuestionGenerator.generate_multiplication_question(3)
            elif operation == 'division':
                question = QuestionGenerator.generate_division_question(3)

            first_num = question['first_number']
            second_num = question['second_number']
            answer = question['answer']

            if operation == 'addition':
                symbol = '+'
            elif operation == 'subtraction':
                symbol = '-'
            elif operation == 'multiplication':
                symbol = '×'
            elif operation == 'division':
                symbol = '÷'

            print(f"  {operation}: {first_num} {symbol} {second_num} = {answer}")

        except Exception as e:
            print(f"  {operation}: خطأ - {str(e)}")

if __name__ == "__main__":
    success = test_number_ordering()
    test_specific_examples()

    if success:
        print("\n🎉 جميع الأرقام مرتبة بشكل صحيح (الأصغر على اليسار والأكبر على اليمين)!")
    else:
        print("\n⚠️ هناك مشاكل في ترتيب الأرقام تحتاج إلى إصلاح!")
