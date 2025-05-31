#!/usr/bin/env python
"""
Test script for participants results export
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')
django.setup()

from competitions.models import Participant, Competition, UserResponse
from competitions.views import export_participants_results_excel
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.http import HttpResponse
import io

def test_participants_export():
    """Test participants results export function"""
    print("🧪 اختبار تصدير نتائج المشاركين...")
    
    # Create a test request
    factory = RequestFactory()
    request = factory.get('/test/')
    
    # Get or create a test user
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@test.com'})
    request.user = user
    
    try:
        # Test participants export
        print("👥 اختبار تصدير نتائج المشاركين...")
        response = export_participants_results_excel(request)
        
        if isinstance(response, HttpResponse):
            print(f"✅ تصدير نتائج المشاركين: نجح - حجم الملف: {len(response.content)} بايت")
            
            # Check content type
            content_type = response.get('Content-Type', '')
            if 'spreadsheet' in content_type:
                print("✅ نوع الملف: Excel صحيح")
            else:
                print(f"⚠️ نوع الملف: {content_type}")
            
            # Check filename
            content_disposition = response.get('Content-Disposition', '')
            if 'نتائج_المشاركين' in content_disposition:
                print("✅ اسم الملف: يحتوي على النص العربي")
            else:
                print(f"⚠️ اسم الملف: {content_disposition}")
                
        else:
            print(f"❌ تصدير نتائج المشاركين: فشل")
            
        # Show some statistics
        print("\n📊 إحصائيات البيانات:")
        print(f"- إجمالي المشاركين: {Participant.objects.count()}")
        print(f"- المشاركين النشطين: {Participant.objects.filter(competitions__is_completed=True).distinct().count()}")
        print(f"- إجمالي المسابقات: {Competition.objects.filter(is_completed=True).count()}")
        print(f"- إجمالي الإجابات: {UserResponse.objects.count()}")
        
        # Show participants by grade
        print("\n📚 المشاركين حسب المستوى:")
        for grade_value, grade_display in Participant.GRADE_CHOICES:
            count = Participant.objects.filter(grade=grade_value).count()
            if count > 0:
                active_count = Participant.objects.filter(
                    grade=grade_value, 
                    competitions__is_completed=True
                ).distinct().count()
                print(f"  - {grade_display}: {count} مشارك ({active_count} نشط)")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_participants_export()
    if success:
        print("\n🎉 اختبار تصدير نتائج المشاركين نجح!")
    else:
        print("\n💥 فشل في اختبار تصدير نتائج المشاركين!")
