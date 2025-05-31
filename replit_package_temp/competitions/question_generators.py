"""
خوارزميات توليد الأسئلة الرياضية للمستويات المختلفة
"""
import random
import math
from fractions import Fraction


class QuestionGenerator:
    """مولد الأسئلة الرياضية للمستويات المختلفة"""

    # تخزين الأسئلة السابقة لتفادي التكرار
    last_questions = []

    @classmethod
    def add_to_history(cls, operation, first_number, second_number):
        """إضافة سؤال إلى سجل الأسئلة السابقة"""
        cls.last_questions.append((operation, first_number, second_number))
        if len(cls.last_questions) > 10:
            cls.last_questions = cls.last_questions[-10:]

    @classmethod
    def _generate_number_excluding_10(cls, min_val, max_val):
        """توليد رقم عشوائي مع استبعاد الرقم 10"""
        while True:
            num = random.randint(min_val, max_val)
            if num != 10:
                return num

    @classmethod
    def _contains_digit_10(cls, number):
        """التحقق من وجود الرقم 10 في العدد"""
        return '10' in str(number)

    @classmethod
    def _is_valid_number(cls, number):
        """التحقق من أن العدد لا يحتوي على الرقم 10"""
        return number != 10 and not cls._contains_digit_10(number)

    @classmethod
    def is_question_repeated(cls, operation, first_number, second_number):
        """التحقق مما إذا كان السؤال مكررًا"""
        for last_op, last_first, last_second in cls.last_questions[-5:]:
            if last_op == operation and last_first == first_number and last_second == second_number:
                return True
            if last_op == operation and last_first == second_number and last_second == first_number:
                return True
        return False

    @classmethod
    def generate_addition_question(cls, difficulty):
        """توليد سؤال جمع حسب المستوى (بدون الرقم 10)"""
        ranges = {
            1: {'min': 1, 'max': 9},   # المستوى الأول (استبعاد 10)
            2: {'min': 3, 'max': 20},  # المستوى الثاني
            3: {'min': 5, 'max': 30},  # المستوى الثالث
            4: {'min': 9, 'max': 40},  # المستوى الرابع
            5: {'min': 21, 'max': 99}, # المستوى الخامس
            6: {'min': 25, 'max': 99}, # المستوى السادس
        }

        range_config = ranges.get(difficulty, ranges[1])
        max_attempts = 50  # زيادة المحاولات لضمان إيجاد أرقام صالحة

        for _ in range(max_attempts):
            # توليد أرقام مع استبعاد الرقم 10
            num1 = cls._generate_number_excluding_10(range_config['min'], range_config['max'])
            num2 = cls._generate_number_excluding_10(range_config['min'], range_config['max'])

            # جعل العدد الأصغر على اليسار والأكبر على اليمين
            first_number = min(num1, num2)
            second_number = max(num1, num2)
            answer = first_number + second_number

            # التأكد من أن الناتج والأرقام صالحة (لا تحتوي على 10)
            if (cls._is_valid_number(first_number) and
                cls._is_valid_number(second_number) and
                cls._is_valid_number(answer) and
                not cls.is_question_repeated("addition", first_number, second_number)):
                break

        cls.add_to_history("addition", first_number, second_number)
        return {
            'first_number': first_number,
            'second_number': second_number,
            'answer': answer
        }

    @classmethod
    def generate_subtraction_question(cls, difficulty):
        """توليد سؤال طرح حسب المستوى (النتيجة موجبة دائماً، بدون الرقم 10)"""
        ranges = {
            1: {'min': 1, 'max': 9},   # المستوى الأول (استبعاد 10)
            2: {'min': 3, 'max': 20},  # المستوى الثاني
            3: {'min': 5, 'max': 30},  # المستوى الثالث
            4: {'min': 9, 'max': 40},  # المستوى الرابع
            5: {'min': 21, 'max': 99}, # المستوى الخامس
            6: {'min': 25, 'max': 99}, # المستوى السادس
        }

        range_config = ranges.get(difficulty, ranges[1])
        max_attempts = 50  # زيادة المحاولات لضمان إيجاد أرقام صالحة

        for _ in range(max_attempts):
            # توليد أرقام مع استبعاد الرقم 10
            num1 = cls._generate_number_excluding_10(range_config['min'], range_config['max'])
            num2 = cls._generate_number_excluding_10(range_config['min'], range_config['max'])

            # ترتيب الأرقام: الأصغر على اليسار والأكبر على اليمين
            # لكن للطرح نحتاج النتيجة موجبة، لذا نطرح الأصغر من الأكبر
            larger_num = max(num1, num2)
            smaller_num = min(num1, num2)

            # العدد الأصغر على اليسار والأكبر على اليمين
            first_number = smaller_num
            second_number = larger_num
            answer = second_number - first_number

            # تجنب النتيجة صفر والتأكد من عدم وجود الرقم 10
            if (answer > 0 and
                cls._is_valid_number(first_number) and
                cls._is_valid_number(second_number) and
                cls._is_valid_number(answer) and
                not cls.is_question_repeated("subtraction", first_number, second_number)):
                break

        cls.add_to_history("subtraction", first_number, second_number)
        return {
            'first_number': first_number,
            'second_number': second_number,
            'answer': answer
        }

    @classmethod
    def generate_multiplication_question(cls, difficulty):
        """توليد سؤال ضرب حسب المستوى (بدون الرقم 10)"""
        ranges = {
            2: {'min': 1, 'max': 4, 'second_min': 1, 'second_max': 9},   # المستوى الثاني: 1×1 إلى 4×9 (استبعاد 10)
            3: {'min': 3, 'max': 11, 'second_min': 3, 'second_max': 9},  # المستوى الثالث: 3×3 إلى 11×9 (استبعاد 10)
            4: {'min': 3, 'max': 12, 'second_min': 3, 'second_max': 12}, # المستوى الرابع: 3 إلى 12
            5: {'min': 7, 'max': 15, 'second_min': 7, 'second_max': 15}, # المستوى الخامس: 7 إلى 15
            6: {'min': 8, 'max': 15, 'second_min': 8, 'second_max': 15}, # المستوى السادس: 8 إلى 15
        }

        range_config = ranges.get(difficulty, ranges[2])
        max_attempts = 50  # زيادة المحاولات لضمان إيجاد أرقام صالحة

        for _ in range(max_attempts):
            # توليد أرقام مع استبعاد الرقم 10
            num1 = cls._generate_number_excluding_10(range_config['min'], range_config['max'])
            num2 = cls._generate_number_excluding_10(range_config['second_min'], range_config['second_max'])

            # جعل العدد الأصغر على اليسار والأكبر على اليمين
            first_number = min(num1, num2)
            second_number = max(num1, num2)
            answer = first_number * second_number

            # التأكد من عدم وجود الرقم 10 في أي من الأرقام أو الناتج
            if (cls._is_valid_number(first_number) and
                cls._is_valid_number(second_number) and
                cls._is_valid_number(answer) and
                not cls.is_question_repeated("multiplication", first_number, second_number)):
                break

        cls.add_to_history("multiplication", first_number, second_number)
        return {
            'first_number': first_number,
            'second_number': second_number,
            'answer': answer
        }

    @classmethod
    def generate_division_question(cls, difficulty):
        """توليد سؤال قسمة حسب المستوى (قسمة صحيحة، بدون الرقم 10)"""
        quotient_ranges = {
            3: [2, 3, 4],           # المستوى الثالث
            4: [3, 4, 5],           # المستوى الرابع
            5: [4, 5, 6, 7],        # المستوى الخامس
            6: [4, 5, 6, 7],        # المستوى السادس
        }

        quotients = quotient_ranges.get(difficulty, [2, 3, 4])
        max_attempts = 50  # زيادة المحاولات لضمان إيجاد أرقام صالحة

        for _ in range(max_attempts):
            # اختيار ناتج القسمة مع استبعاد الرقم 10
            quotient = random.choice([q for q in quotients if q != 10])
            # توليد المقسوم عليه مع استبعاد الرقم 10
            divisor = cls._generate_number_excluding_10(2, 12)
            dividend = quotient * divisor

            # للقسمة: العدد الأصغر (المقسوم عليه) على اليسار والأكبر (المقسوم) على اليمين
            first_number = divisor
            second_number = dividend
            answer = quotient

            # التأكد من عدم وجود الرقم 10 في أي من الأرقام
            if (cls._is_valid_number(first_number) and
                cls._is_valid_number(second_number) and
                cls._is_valid_number(answer) and
                not cls.is_question_repeated("division", first_number, second_number)):
                break

        cls.add_to_history("division", first_number, second_number)
        return {
            'first_number': first_number,
            'second_number': second_number,
            'answer': answer
        }

    @classmethod
    def generate_mixed_operations_question(cls, difficulty):
        """توليد سؤال عمليات مختلطة للمرحلة الثانية"""
        if difficulty == 7:  # المستوى الأول - المرحلة الثانية
            return cls._generate_integer_operations_question()
        else:
            return cls._generate_priority_operations_question()

    @classmethod
    def _generate_integer_operations_question(cls):
        """توليد سؤال عمليات على الأعداد الصحيحة الموجبة والسالبة"""
        operations = ['+', '-', '*', '/']
        operation = random.choice(operations[:2])  # جمع وطرح فقط للبداية

        num1 = random.randint(-20, 20)
        num2 = random.randint(-20, 20)

        # جعل العدد الأصغر على اليسار والأكبر على اليمين
        if abs(num1) <= abs(num2):
            first_number = num1
            second_number = num2
        else:
            first_number = num2
            second_number = num1

        if operation == '+':
            answer = first_number + second_number
        else:  # operation == '-'
            answer = first_number - second_number

        return {
            'first_number': first_number,
            'second_number': second_number,
            'answer': answer,
            'operation_symbol': operation
        }

    @classmethod
    def _generate_priority_operations_question(cls):
        """توليد سؤال قواعد أولوية العمليات"""
        # مثال: 5 + 3 × 2
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        num3 = random.randint(1, 10)

        # 5 + 3 × 2 = 5 + 6 = 11
        answer = num1 + (num2 * num3)

        return {
            'expression': f"{num1} + {num2} × {num3}",
            'answer': answer
        }

    @classmethod
    def generate_fractions_question(cls):
        """توليد سؤال كسور وأعداد عشرية"""
        # مثال بسيط: جمع كسرين
        num1 = random.randint(1, 5)
        den1 = random.randint(2, 8)
        num2 = random.randint(1, 5)
        den2 = den1  # نفس المقام للتبسيط

        frac1 = Fraction(num1, den1)
        frac2 = Fraction(num2, den2)
        answer = frac1 + frac2

        return {
            'expression': f"{frac1} + {frac2}",
            'answer': float(answer)
        }

    @classmethod
    def generate_algebra_question(cls):
        """توليد سؤال جبر (معادلات من الدرجة الأولى)"""
        # مثال: 2x + 3 = 11, x = ?
        coefficient = random.randint(2, 5)
        constant = random.randint(1, 10)
        result = random.randint(10, 30)

        # 2x + 3 = 11 => x = (11-3)/2 = 4
        x_value = (result - constant) / coefficient

        return {
            'expression': f"{coefficient}x + {constant} = {result}",
            'answer': x_value
        }

    @classmethod
    def generate_geometry_question(cls):
        """توليد سؤال هندسة (مساحات بسيطة)"""
        shape_type = random.choice(['rectangle', 'triangle'])

        if shape_type == 'rectangle':
            length = random.randint(3, 12)
            width = random.randint(2, 10)
            area = length * width
            return {
                'expression': f"مساحة مستطيل طوله {length} وعرضه {width}",
                'answer': area
            }
        else:  # triangle
            base = random.randint(4, 12)
            height = random.randint(3, 10)
            area = (base * height) / 2
            return {
                'expression': f"مساحة مثلث قاعدته {base} وارتفاعه {height}",
                'answer': area
            }

    @classmethod
    def generate_trigonometry_question(cls):
        """توليد سؤال مثلثات (النسب المثلثية البسيطة)"""
        # زوايا خاصة
        angles = [30, 45, 60]
        angle = random.choice(angles)
        trig_func = random.choice(['sin', 'cos'])

        values = {
            ('sin', 30): 0.5,
            ('sin', 45): 0.707,
            ('sin', 60): 0.866,
            ('cos', 30): 0.866,
            ('cos', 45): 0.707,
            ('cos', 60): 0.5,
        }

        answer = values.get((trig_func, angle), 0.5)

        return {
            'expression': f"{trig_func}({angle}°)",
            'answer': round(answer, 3)
        }

    @classmethod
    def generate_word_problem(cls, difficulty):
        """توليد مسألة تطبيقية"""
        problem_types = ['speed', 'percentage', 'proportion']
        problem_type = random.choice(problem_types)

        if problem_type == 'speed':
            distance = random.randint(60, 300)
            time = random.randint(2, 8)
            speed = distance / time
            return {
                'expression': f"سيارة قطعت {distance} كم في {time} ساعات. ما سرعتها؟",
                'answer': speed
            }
        elif problem_type == 'percentage':
            total = random.randint(100, 500)
            percentage = random.randint(10, 50)
            result = (total * percentage) / 100
            return {
                'expression': f"احسب {percentage}% من {total}",
                'answer': result
            }
        else:  # proportion
            a = random.randint(2, 8)
            b = random.randint(3, 9)
            c = random.randint(4, 12)
            x = (b * c) / a
            return {
                'expression': f"إذا كان {a} : {b} = {c} : x، فإن x = ؟",
                'answer': x
            }
