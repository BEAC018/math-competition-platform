#!/usr/bin/env python
"""
Test script for URL endpoints
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

def test_export_urls():
    """Test export URL endpoints"""
    print("🔗 اختبار روابط التصدير...")
    
    # Create test client
    client = Client()
    
    # Get or create a test user
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@test.com'})
    
    # Login the user
    client.force_login(user)
    
    # Test URLs
    urls_to_test = [
        ('competitions:export_grade_analytics_excel', 'تصدير تحليلات المستويات'),
        ('competitions:export_operations_analytics_excel', 'تصدير تحليلات العمليات'),
        ('competitions:export_general_analytics_excel', 'تصدير التحليلات العامة'),
    ]
    
    results = []
    
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"📊 اختبار {description}: {url}")
            
            response = client.get(url)
            
            if response.status_code == 200:
                content_type = response.get('Content-Type', '')
                content_length = len(response.content)
                
                if 'spreadsheet' in content_type:
                    print(f"✅ {description}: نجح - Excel file ({content_length} bytes)")
                    results.append(True)
                else:
                    print(f"⚠️ {description}: نجح لكن نوع المحتوى غير متوقع: {content_type}")
                    results.append(True)
            else:
                print(f"❌ {description}: فشل - Status: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"💥 {description}: خطأ - {str(e)}")
            results.append(False)
    
    # Test chart data API
    chart_apis = [
        ('competitions:get_chart_data', 'grade_stats', 'بيانات المستويات'),
        ('competitions:get_chart_data', 'operations_stats', 'بيانات العمليات'),
        ('competitions:get_chart_data', 'time_trends', 'الاتجاهات الزمنية'),
    ]
    
    print("\n🔌 اختبار API endpoints:")
    for url_name, chart_type, description in chart_apis:
        try:
            url = reverse(url_name, args=[chart_type])
            print(f"📈 اختبار {description}: {url}")
            
            response = client.get(url)
            
            if response.status_code == 200:
                content_type = response.get('Content-Type', '')
                if 'json' in content_type:
                    print(f"✅ {description}: نجح - JSON response")
                    results.append(True)
                else:
                    print(f"⚠️ {description}: نجح لكن نوع المحتوى غير متوقع: {content_type}")
                    results.append(True)
            else:
                print(f"❌ {description}: فشل - Status: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"💥 {description}: خطأ - {str(e)}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n📊 معدل النجاح: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    
    return all(results)

if __name__ == "__main__":
    success = test_export_urls()
    if success:
        print("\n🎉 جميع الروابط تعمل بشكل صحيح!")
    else:
        print("\n⚠️ بعض الروابط تحتاج إلى مراجعة!")
