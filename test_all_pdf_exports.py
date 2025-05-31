#!/usr/bin/env python
"""
Test script for all PDF export functions
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')
django.setup()

from competitions.models import Participant, Competition, UserResponse
from competitions.views import export_history_pdf, export_analytics_pdf
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import HttpResponse
import io

def test_all_pdf_exports():
    """Test all PDF export functions"""
    print("🧪 اختبار جميع دوال تصدير PDF...")
    
    # Create a test request
    factory = RequestFactory()
    request = factory.get('/test/')
    
    # Get or create a test user
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@test.com'})
    request.user = user
    
    results = []
    
    # Test functions
    pdf_functions = [
        (export_history_pdf, 'تصدير سجل المسابقات PDF'),
        (export_analytics_pdf, 'تصدير التحليلات PDF'),
    ]
    
    for func, description in pdf_functions:
        try:
            print(f"\n📄 اختبار {description}...")
            response = func(request)
            
            if isinstance(response, HttpResponse):
                content_type = response.get('Content-Type', '')
                content_length = len(response.content)
                
                if 'pdf' in content_type:
                    print(f"✅ {description}: نجح - حجم الملف: {content_length} بايت")
                    results.append(True)
                else:
                    print(f"⚠️ {description}: نوع المحتوى غير متوقع: {content_type}")
                    results.append(False)
            else:
                print(f"❌ {description}: فشل - استجابة غير صحيحة")
                results.append(False)
                
        except Exception as e:
            print(f"💥 {description}: خطأ - {str(e)}")
            results.append(False)
    
    # Show statistics
    print("\n📊 إحصائيات البيانات:")
    print(f"- إجمالي المسابقات: {Competition.objects.filter(user=user, is_completed=True).count()}")
    print(f"- إجمالي الإجابات: {UserResponse.objects.filter(competition__user=user).count()}")
    print(f"- إجمالي المشاركين: {Participant.objects.count()}")
    
    # Summary
    success_rate = sum(results) / len(results) * 100
    print(f"\n📈 معدل النجاح: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    
    return all(results)

if __name__ == "__main__":
    success = test_all_pdf_exports()
    if success:
        print("\n🎉 جميع اختبارات PDF نجحت!")
    else:
        print("\n⚠️ بعض اختبارات PDF تحتاج إلى مراجعة!")
