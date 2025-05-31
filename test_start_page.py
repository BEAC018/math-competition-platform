#!/usr/bin/env python
"""
Test script for start competition page
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

def test_start_page():
    """Test start competition page"""
    print("🧪 اختبار صفحة بدء المسابقة...")
    
    # Create test client
    client = Client()
    
    # Get or create a test user
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@test.com'})
    
    # Login the user
    client.force_login(user)
    
    try:
        # Test start competition page
        url = reverse('competitions:start_competition')
        print(f"📊 اختبار صفحة بدء المسابقة: {url}")
        
        response = client.get(url)
        
        if response.status_code == 200:
            print(f"✅ صفحة بدء المسابقة: نجحت - Status: {response.status_code}")
            
            # Check if the page contains expected content
            content = response.content.decode('utf-8')
            
            checks = [
                ('بدء مسابقة جديدة', 'عنوان الصفحة'),
                ('إضافة مشارك جديد', 'زر إضافة مشارك'),
                ('المرحلة الأولى', 'المراحل'),
                ('اختيار المستوى الدراسي', 'اختيار المستوى'),
                ('ابدأ المسابقة', 'زر البدء'),
            ]
            
            for check_text, description in checks:
                if check_text in content:
                    print(f"  ✅ {description}: موجود")
                else:
                    print(f"  ❌ {description}: مفقود")
            
            return True
        else:
            print(f"❌ صفحة بدء المسابقة: فشلت - Status: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"محتوى الخطأ: {response.content.decode('utf-8')[:500]}...")
            return False
            
    except Exception as e:
        print(f"💥 خطأ في اختبار صفحة بدء المسابقة: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_start_page()
    if success:
        print("\n🎉 صفحة بدء المسابقة تعمل بشكل صحيح!")
    else:
        print("\n⚠️ صفحة بدء المسابقة تحتاج إلى مراجعة!")
