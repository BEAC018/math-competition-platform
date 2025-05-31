#!/usr/bin/env python
"""
Test script for PDF export fix
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')
django.setup()

from competitions.models import Participant, Competition, UserResponse
from competitions.views import export_history_pdf
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import HttpResponse
import io

def test_pdf_export():
    """Test PDF export function"""
    print("🧪 اختبار تصدير PDF...")
    
    # Create a test request
    factory = RequestFactory()
    request = factory.get('/test/')
    
    # Get or create a test user
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@test.com'})
    request.user = user
    
    try:
        # Test PDF export
        print("📄 اختبار تصدير PDF...")
        response = export_history_pdf(request)
        
        if isinstance(response, HttpResponse):
            print(f"✅ تصدير PDF: نجح - حجم الملف: {len(response.content)} بايت")
            
            # Check content type
            content_type = response.get('Content-Type', '')
            if 'pdf' in content_type:
                print("✅ نوع الملف: PDF صحيح")
            else:
                print(f"⚠️ نوع الملف: {content_type}")
            
            # Check filename
            content_disposition = response.get('Content-Disposition', '')
            if 'competition_history' in content_disposition:
                print("✅ اسم الملف: يحتوي على اسم مناسب")
            else:
                print(f"⚠️ اسم الملف: {content_disposition}")
                
        else:
            print(f"❌ تصدير PDF: فشل")
            
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
    success = test_pdf_export()
    if success:
        print("\n🎉 اختبار تصدير PDF نجح!")
    else:
        print("\n💥 فشل في اختبار تصدير PDF!")
