#!/usr/bin/env python
"""
Script to create sample analytics data for testing the advanced analytics system
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
import random

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')
django.setup()

from competitions.models import Participant, Competition, MathQuestion, UserResponse, CompetitionResult
from accounts.models import User

def create_sample_data():
    """Create sample data for analytics testing"""

    # Create sample participants if they don't exist
    participants_data = [
        {'name': 'أحمد محمد', 'grade': '1'},
        {'name': 'فاطمة علي', 'grade': '2'},
        {'name': 'محمد حسن', 'grade': '3'},
        {'name': 'عائشة أحمد', 'grade': '4'},
        {'name': 'علي محمود', 'grade': '5'},
        {'name': 'زينب سالم', 'grade': '6'},
        {'name': 'يوسف عبدالله', 'grade': '7'},
        {'name': 'مريم خالد', 'grade': '8'},
        {'name': 'عمر سعيد', 'grade': '9'},
        {'name': 'نور الدين', 'grade': '1'},
        {'name': 'سارة محمد', 'grade': '2'},
        {'name': 'حسام علي', 'grade': '3'},
        {'name': 'ليلى أحمد', 'grade': '4'},
        {'name': 'كريم محمود', 'grade': '5'},
        {'name': 'هدى سالم', 'grade': '6'},
    ]

    created_participants = []
    for data in participants_data:
        participant, created = Participant.objects.get_or_create(
            name=data['name'],
            defaults={'grade': data['grade']}
        )
        created_participants.append(participant)
        if created:
            print(f"Created participant: {participant.name}")

    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='analytics_test_user',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('testpassword123')
        user.save()
        print(f"Created test user: {user.username}")

    # Create sample math questions for different operations
    operations = ['addition', 'subtraction', 'multiplication', 'division']
    sample_questions = []

    for operation in operations:
        for difficulty in range(1, 10):  # 9 difficulty levels
            for _ in range(5):  # 5 questions per operation per difficulty
                if operation == 'addition':
                    operand1 = random.randint(1, 10 * difficulty)
                    operand2 = random.randint(1, 10 * difficulty)
                    correct_answer = operand1 + operand2
                elif operation == 'subtraction':
                    operand1 = random.randint(10 * difficulty, 20 * difficulty)
                    operand2 = random.randint(1, operand1)
                    correct_answer = operand1 - operand2
                elif operation == 'multiplication':
                    operand1 = random.randint(1, 12)
                    operand2 = random.randint(1, 12)
                    correct_answer = operand1 * operand2
                elif operation == 'division':
                    operand2 = random.randint(2, 12)
                    correct_answer = random.randint(1, 20)
                    operand1 = operand2 * correct_answer

                # Check if question already exists
                existing_question = MathQuestion.objects.filter(
                    operation=operation,
                    first_number=operand1,
                    second_number=operand2,
                    difficulty=difficulty
                ).first()

                if existing_question:
                    question = existing_question
                    created = False
                else:
                    question = MathQuestion.objects.create(
                        operation=operation,
                        first_number=operand1,
                        second_number=operand2,
                        difficulty=difficulty,
                        answer=correct_answer
                    )
                    created = True
                sample_questions.append(question)
                if created:
                    print(f"Created question: {operand1} {operation} {operand2} = {correct_answer}")

    # Create sample competitions and responses
    for participant in created_participants[:10]:  # Use first 10 participants
        # Create 3-5 competitions per participant
        num_competitions = random.randint(3, 5)

        for comp_num in range(num_competitions):
            # Create competition
            start_time = timezone.now() - timedelta(days=random.randint(1, 30))
            end_time = start_time + timedelta(minutes=random.randint(5, 15))
            difficulty = random.randint(1, 9)

            competition = Competition.objects.create(
                user=user,
                participant=participant,
                difficulty=difficulty,
                start_time=start_time,
                end_time=end_time,
                is_completed=True
            )

            # Create 15 responses per competition
            questions_for_difficulty = [q for q in sample_questions if q.difficulty == difficulty]
            selected_questions = random.sample(questions_for_difficulty, min(15, len(questions_for_difficulty)))

            total_correct = 0
            for i, question in enumerate(selected_questions):
                # Simulate different accuracy rates based on operation and participant grade
                base_accuracy = 0.7  # 70% base accuracy

                # Adjust accuracy based on operation difficulty
                if question.operation == 'addition':
                    accuracy = base_accuracy + 0.2
                elif question.operation == 'subtraction':
                    accuracy = base_accuracy + 0.1
                elif question.operation == 'multiplication':
                    accuracy = base_accuracy
                elif question.operation == 'division':
                    accuracy = base_accuracy - 0.1

                # Adjust accuracy based on participant grade vs question difficulty
                grade_num = int(participant.grade)
                if grade_num >= difficulty:
                    accuracy += 0.1
                else:
                    accuracy -= 0.1

                # Ensure accuracy is between 0 and 1
                accuracy = max(0.3, min(0.95, accuracy))

                # Determine if answer is correct
                is_correct = random.random() < accuracy

                # Generate response time (faster for easier questions/higher grades)
                base_time = 12.0  # 12 seconds base
                time_variation = random.uniform(-3, 5)
                if grade_num >= difficulty:
                    time_variation -= 2
                if question.operation in ['addition', 'subtraction']:
                    time_variation -= 1

                response_time = max(3.0, base_time + time_variation)

                # Create user response
                user_answer = question.answer if is_correct else question.answer + random.randint(-10, 10)

                UserResponse.objects.create(
                    competition=competition,
                    question=question,
                    user_answer=user_answer,
                    is_correct=is_correct,
                    response_time=response_time
                )

                if is_correct:
                    total_correct += 1

            # Create competition result
            total_score = total_correct * 3  # 3 points per correct answer
            CompetitionResult.objects.create(
                competition=competition,
                total_score=total_score
            )

            print(f"Created competition for {participant.name}: {total_correct}/{len(selected_questions)} correct")

    print("\n✅ Sample analytics data created successfully!")
    print(f"📊 Created data for {len(created_participants)} participants")
    print(f"🧮 Created {len(sample_questions)} math questions")
    print(f"🏆 Created competitions with responses and results")
    print("\n🔗 You can now test the analytics at:")
    print("   - Advanced Analytics: /analytics/")
    print("   - Participant Profiles: /participant/<id>/")

if __name__ == '__main__':
    create_sample_data()
