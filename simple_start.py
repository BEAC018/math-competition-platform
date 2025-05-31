#!/usr/bin/env python3
"""
🚀 بدء بسيط للمنصة
Simple platform start
"""

import subprocess
import sys
import time

def main():
    print("🎯 بدء تشغيل منصة المسابقات الرياضية")
    print("="*50)
    
    try:
        # إغلاق ngrok السابق
        print("🔄 إغلاق العمليات السابقة...")
        from pyngrok import ngrok
        ngrok.kill()
        time.sleep(2)
        
        # إنشاء نفق جديد
        print("🌐 إنشاء رابط جديد...")
        public_url = ngrok.connect(8000)
        clean_url = str(public_url).split('"')[1]
        
        print("\n" + "="*60)
        print("🎉 رابط جديد جاهز!")
        print("="*60)
        print(f"🌐 الرابط: {clean_url}")
        print(f"👥 للتلاميذ: {clean_url}/student/login/")
        print(f"👨‍🏫 للأساتذة: {clean_url}/accounts/login/")
        print(f"🔑 الرمز: ben25")
        print("="*60)
        
        # حفظ الرابط
        with open("LIVE_URL.txt", "w", encoding='utf-8') as f:
            f.write(f"الرابط الحالي: {clean_url}\n")
            f.write(f"للتلاميذ: {clean_url}/student/login/\n")
            f.write(f"للأساتذة: {clean_url}/accounts/login/\n")
            f.write(f"الرمز: ben25\n")
        
        # رسالة للمشاركة
        message = f"""🎯 منصة المسابقات الرياضية

🌐 الرابط: {clean_url}/student/login/
🔑 الرمز: ben25

📝 الخطوات:
1. انقر الرابط
2. اكتب اسمك
3. اكتب الرمز: ben25
4. اختر مستواك
5. ابدأ!

🎮 استمتعوا! 🚀"""

        with open("SHARE_MESSAGE.txt", "w", encoding='utf-8') as f:
            f.write(message)
        
        print("📄 تم حفظ الروابط في LIVE_URL.txt")
        print("📱 تم حفظ رسالة المشاركة في SHARE_MESSAGE.txt")
        
        print("\n🚀 تشغيل الخادم...")
        subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
        
    except KeyboardInterrupt:
        print("\n✅ تم إيقاف المنصة")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    main()
