#!/usr/bin/env python
"""
Simple test for number ordering
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')
django.setup()

from competitions.question_generators import QuestionGenerator
from competitions.views import generate_math_question

def test_simple_examples():
    """Test simple examples to see the ordering"""
    print("🔍 أمثلة بسيطة للترتيب الجديد:")
    
    operations = ['addition', 'subtraction', 'multiplication', 'division']
    
    for operation in operations:
        print(f"\n📊 {operation.upper()}:")
        
        for i in range(5):
            try:
                # Test QuestionGenerator
                if operation == 'addition':
                    question = QuestionGenerator.generate_addition_question(2)
                elif operation == 'subtraction':
                    question = QuestionGenerator.generate_subtraction_question(2)
                elif operation == 'multiplication':
                    question = QuestionGenerator.generate_multiplication_question(2)
                elif operation == 'division':
                    question = QuestionGenerator.generate_division_question(3)
                
                first_num = question['first_number']
                second_num = question['second_number']
                answer = question['answer']
                
                if operation == 'addition':
                    symbol = '+'
                    check = first_num + second_num
                elif operation == 'subtraction':
                    symbol = '-'
                    check = second_num - first_num  # الأكبر - الأصغر
                elif operation == 'multiplication':
                    symbol = '×'
                    check = first_num * second_num
                elif operation == 'division':
                    symbol = '÷'
                    check = second_num // first_num  # المقسوم ÷ المقسوم عليه
                
                order_status = "✅" if first_num <= second_num else "❌"
                answer_status = "✅" if check == answer else "❌"
                
                print(f"  {order_status} {answer_status} QuestionGenerator: {first_num} {symbol} {second_num} = {answer} (تحقق: {check})")
                
            except Exception as e:
                print(f"  ❌ خطأ في QuestionGenerator {operation}: {str(e)}")
        
        # Test views.py function
        print(f"\n📊 views.py {operation.upper()}:")
        for i in range(5):
            try:
                question = generate_math_question(operation, 2)
                
                first_num = question['first_number']
                second_num = question['second_number']
                answer = question['answer']
                
                if operation == 'addition':
                    symbol = '+'
                    check = first_num + second_num
                elif operation == 'subtraction':
                    symbol = '-'
                    check = second_num - first_num  # الأكبر - الأصغر
                elif operation == 'multiplication':
                    symbol = '×'
                    check = first_num * second_num
                elif operation == 'division':
                    symbol = '÷'
                    check = second_num // first_num  # المقسوم ÷ المقسوم عليه
                
                order_status = "✅" if first_num <= second_num else "❌"
                answer_status = "✅" if check == answer else "❌"
                
                print(f"  {order_status} {answer_status} views.py: {first_num} {symbol} {second_num} = {answer} (تحقق: {check})")
                
            except Exception as e:
                print(f"  ❌ خطأ في views.py {operation}: {str(e)}")

if __name__ == "__main__":
    test_simple_examples()
    print("\n💡 الترتيب المطلوب: العدد الأصغر على اليسار والأكبر على اليمين")
