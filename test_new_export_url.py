#!/usr/bin/env python
"""
Test script for new export URL
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

def test_new_export_url():
    """Test new participants export URL"""
    print("🔗 اختبار رابط تصدير نتائج المشاركين...")
    
    # Create test client
    client = Client()
    
    # Get or create a test user
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@test.com'})
    
    # Login the user
    client.force_login(user)
    
    try:
        # Test new export URL
        url = reverse('competitions:export_participants_results_excel')
        print(f"📊 اختبار رابط تصدير نتائج المشاركين: {url}")
        
        response = client.get(url)
        
        if response.status_code == 200:
            content_type = response.get('Content-Type', '')
            content_length = len(response.content)
            
            if 'spreadsheet' in content_type:
                print(f"✅ تصدير نتائج المشاركين: نجح - Excel file ({content_length} bytes)")
                
                # Check if file has reasonable size (should be larger than basic exports)
                if content_length > 10000:  # More than 10KB indicates multiple sheets
                    print("✅ حجم الملف: يشير إلى وجود بيانات متعددة الأوراق")
                else:
                    print(f"⚠️ حجم الملف صغير: {content_length} bytes")
                
                return True
            else:
                print(f"⚠️ نوع المحتوى غير متوقع: {content_type}")
                return False
        else:
            print(f"❌ فشل في الوصول للرابط - Status: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"محتوى الخطأ: {response.content.decode('utf-8')[:200]}...")
            return False
            
    except Exception as e:
        print(f"💥 خطأ في اختبار الرابط: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_new_export_url()
    if success:
        print("\n🎉 رابط تصدير نتائج المشاركين يعمل بشكل صحيح!")
    else:
        print("\n⚠️ رابط تصدير نتائج المشاركين يحتاج إلى مراجعة!")
