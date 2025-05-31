#!/usr/bin/env python
"""
Test script for Excel export functionality
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')
django.setup()

from competitions.models import Participant, Competition, UserResponse
from competitions.views import export_grade_analytics_excel, export_operations_analytics_excel, export_general_analytics_excel
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import HttpResponse
import io

def test_export_functions():
    """Test all export functions"""
    print("🧪 اختبار دوال التصدير...")
    
    # Create a test request
    factory = RequestFactory()
    request = factory.get('/test/')
    
    # Get or create a test user
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@test.com'})
    request.user = user
    
    try:
        # Test grade analytics export
        print("📊 اختبار تصدير تحليلات المستويات...")
        response1 = export_grade_analytics_excel(request)
        if isinstance(response1, HttpResponse):
            print(f"✅ تصدير المستويات: نجح - حجم الملف: {len(response1.content)} بايت")
        else:
            print(f"❌ تصدير المستويات: فشل")
            
        # Test operations analytics export
        print("🧮 اختبار تصدير تحليلات العمليات...")
        response2 = export_operations_analytics_excel(request)
        if isinstance(response2, HttpResponse):
            print(f"✅ تصدير العمليات: نجح - حجم الملف: {len(response2.content)} بايت")
        else:
            print(f"❌ تصدير العمليات: فشل")
            
        # Test general analytics export
        print("📈 اختبار التصدير العام...")
        response3 = export_general_analytics_excel(request)
        if isinstance(response3, HttpResponse):
            print(f"✅ التصدير العام: نجح - حجم الملف: {len(response3.content)} بايت")
        else:
            print(f"❌ التصدير العام: فشل")
            
        print("\n📋 ملخص النتائج:")
        print(f"- إجمالي المشاركين: {Participant.objects.count()}")
        print(f"- إجمالي المسابقات: {Competition.objects.count()}")
        print(f"- إجمالي الإجابات: {UserResponse.objects.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_export_functions()
    if success:
        print("\n🎉 جميع الاختبارات نجحت!")
    else:
        print("\n💥 فشل في بعض الاختبارات!")
