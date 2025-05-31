from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('competitions/score_display.html')
def display_score(result, show_details=True, size='normal'):
    """
    عرض النتيجة بالصيغة الموحدة مع جميع النسب
    
    Args:
        result: كائن CompetitionResult
        show_details: عرض التفاصيل الكاملة أم لا
        size: حجم العرض ('small', 'normal', 'large')
    """
    if not result:
        return {'result': None}
    
    score_data = result.get_formatted_score_display()
    
    return {
        'result': result,
        'score_data': score_data,
        'show_details': show_details,
        'size': size
    }

@register.simple_tag
def score_color_class(score, total=45):
    """تحديد لون النتيجة حسب النسبة المئوية"""
    if total == 0:
        return 'text-muted'
    
    percentage = (score / total) * 100
    if percentage >= 75:
        return 'text-success'  # أخضر
    elif percentage >= 50:
        return 'text-warning'  # أصفر
    else:
        return 'text-danger'   # أحمر

@register.simple_tag
def score_badge_class(score, total=45):
    """تحديد نوع الشارة حسب النسبة المئوية"""
    if total == 0:
        return 'bg-secondary'
    
    percentage = (score / total) * 100
    if percentage >= 75:
        return 'bg-success'  # أخضر
    elif percentage >= 50:
        return 'bg-warning'  # أصفر
    else:
        return 'bg-danger'   # أحمر

@register.simple_tag
def calculate_percentage(score, total, target_scale=100):
    """حساب النسبة المئوية لمقياس معين"""
    if total == 0:
        return 0
    return round((score / total) * target_scale, 1)

@register.simple_tag
def performance_level(score, total=45):
    """تحديد مستوى الأداء"""
    if total == 0:
        return 'غير محدد'
    
    percentage = (score / total) * 100
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

@register.simple_tag
def performance_emoji(score, total=45):
    """رمز تعبيري للأداء"""
    if total == 0:
        return '❓'
    
    percentage = (score / total) * 100
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

@register.inclusion_tag('competitions/score_summary.html')
def score_summary(score, total=45, title="النتيجة"):
    """عرض ملخص النتيجة بجميع المقاييس"""
    if total == 0:
        return {
            'score': 0,
            'total': total,
            'title': title,
            'percentage_100': 0,
            'percentage_10': 0,
            'percentage_20': 0,
            'color_class': 'text-muted',
            'badge_class': 'bg-secondary',
            'performance_level': 'غير محدد',
            'performance_emoji': '❓'
        }
    
    percentage_100 = round((score / total) * 100, 1)
    percentage_10 = round((score / total) * 10, 1)
    percentage_20 = round((score / total) * 20, 1)
    
    # تحديد اللون
    if percentage_100 >= 75:
        color_class = 'text-success'
        badge_class = 'bg-success'
    elif percentage_100 >= 50:
        color_class = 'text-warning'
        badge_class = 'bg-warning'
    else:
        color_class = 'text-danger'
        badge_class = 'bg-danger'
    
    # تحديد مستوى الأداء
    if percentage_100 >= 90:
        performance_level = 'ممتاز'
        performance_emoji = '🌟'
    elif percentage_100 >= 75:
        performance_level = 'جيد جداً'
        performance_emoji = '😊'
    elif percentage_100 >= 60:
        performance_level = 'جيد'
        performance_emoji = '🙂'
    elif percentage_100 >= 50:
        performance_level = 'مقبول'
        performance_emoji = '😐'
    else:
        performance_level = 'ضعيف'
        performance_emoji = '😞'
    
    return {
        'score': score,
        'total': total,
        'title': title,
        'percentage_100': percentage_100,
        'percentage_10': percentage_10,
        'percentage_20': percentage_20,
        'color_class': color_class,
        'badge_class': badge_class,
        'performance_level': performance_level,
        'performance_emoji': performance_emoji
    }

@register.filter
def multiply(value, arg):
    """ضرب قيمة في رقم آخر"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """قسمة قيمة على رقم آخر"""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0
