#!/usr/bin/env python
"""
Test script for history export fix
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')
django.setup()

from competitions.models import Participant, Competition, UserResponse
from competitions.views import export_history_excel
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import HttpResponse
import io

def test_history_export():
    """Test history export function"""
    print("🧪 اختبار تصدير سجل المسابقات...")
    
    # Create a test request
    factory = RequestFactory()
    request = factory.get('/test/')
    
    # Get or create a test user
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@test.com'})
    request.user = user
    
    try:
        # Test history export
        print("📊 اختبار تصدير سجل المسابقات...")
        response = export_history_excel(request)
        
        if isinstance(response, HttpResponse):
            print(f"✅ تصدير سجل المسابقات: نجح - حجم الملف: {len(response.content)} بايت")
            
            # Check content type
            content_type = response.get('Content-Type', '')
            if 'spreadsheet' in content_type:
                print("✅ نوع الملف: Excel صحيح")
            else:
                print(f"⚠️ نوع الملف: {content_type}")
            
            # Check filename
            content_disposition = response.get('Content-Disposition', '')
            if 'سجل_المسابقات' in content_disposition:
                print("✅ اسم الملف: يحتوي على النص العربي")
            else:
                print(f"⚠️ اسم الملف: {content_disposition}")
                
        else:
            print(f"❌ تصدير سجل المسابقات: فشل")
            
        # Show some statistics
        print("\n📊 إحصائيات البيانات:")
        print(f"- إجمالي المسابقات: {Competition.objects.filter(user=user, is_completed=True).count()}")
        print(f"- إجمالي الإجابات: {UserResponse.objects.filter(competition__user=user).count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_history_export()
    if success:
        print("\n🎉 اختبار تصدير سجل المسابقات نجح!")
    else:
        print("\n💥 فشل في اختبار تصدير سجل المسابقات!")
