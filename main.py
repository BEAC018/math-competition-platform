#!/usr/bin/env python3
"""
📱 تطبيق المسابقات الرياضية للهاتف النقال
Mobile Math Competition App - Main Entry Point
"""

# استيراد التطبيق الرئيسي
try:
    from mobile_app_simple import MathCompetitionApp
except ImportError:
    try:
        from mobile_app import MathCompetitionApp
    except ImportError:
        print("❌ خطأ: لا يمكن استيراد التطبيق")
        exit(1)

if __name__ == '__main__':
    # تشغيل التطبيق
    MathCompetitionApp().run()
