#!/usr/bin/env python3
"""
🔄 إعادة تشغيل المنصة مع رابط جديد
Restart platform with new URL
"""

import subprocess
import sys
import time
import threading
import os

def get_new_ngrok_url():
    """الحصول على رابط ngrok جديد"""
    try:
        from pyngrok import ngrok
        
        # إغلاق جميع الأنفاق السابقة
        ngrok.kill()
        time.sleep(2)
        
        # إنشاء نفق جديد
        print("🌐 إنشاء رابط جديد...")
        public_url = ngrok.connect(8000)
        
        # استخراج الرابط النظيف
        clean_url = str(public_url).split('"')[1]
        
        print("\n" + "="*60)
        print("🎉 تم إنشاء رابط جديد بنجاح!")
        print("="*60)
        print(f"🌐 الرابط الجديد: {clean_url}")
        print(f"👥 رابط التلاميذ: {clean_url}/student/login/")
        print(f"👨‍🏫 رابط الأساتذة: {clean_url}/accounts/login/")
        print(f"🔑 رمز دخول التلاميذ: ben25")
        print("="*60)
        
        # حفظ الرابط الجديد
        with open("CURRENT_URL.txt", "w", encoding='utf-8') as f:
            f.write(f"الرابط الحالي: {clean_url}\n")
            f.write(f"رابط التلاميذ: {clean_url}/student/login/\n")
            f.write(f"رابط الأساتذة: {clean_url}/accounts/login/\n")
            f.write(f"رمز الدخول: ben25\n")
            f.write(f"تاريخ التحديث: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # إنشاء رسالة جديدة للمشاركة
        whatsapp_message = f"""🎯 منصة المسابقات الرياضية - رابط محدث

🌐 الرابط الجديد:
{clean_url}/student/login/

🔑 رمز الدخول: ben25

📝 خطوات الدخول:
1️⃣ انقر على الرابط أعلاه
2️⃣ اكتب اسمك الكامل
3️⃣ اكتب رمز الدخول: ben25
4️⃣ اختر مستواك الدراسي (1-9)
5️⃣ ابدأ المسابقة!

🎮 استمتعوا بالتعلم! 🚀"""

        with open("NEW_SHARE_MESSAGE.txt", "w", encoding='utf-8') as f:
            f.write(whatsapp_message)
        
        print("📄 تم حفظ الرابط الجديد في CURRENT_URL.txt")
        print("📱 تم حفظ رسالة المشاركة في NEW_SHARE_MESSAGE.txt")
        
        return clean_url
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء الرابط: {e}")
        return None

def start_django_server():
    """تشغيل خادم Django"""
    print("🚀 تشغيل خادم Django...")
    try:
        subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
    except KeyboardInterrupt:
        print("\n✅ تم إيقاف الخادم")
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")

def create_auto_restart_script():
    """إنشاء سكريبت إعادة التشغيل التلقائي"""
    script_content = '''#!/usr/bin/env python3
import subprocess
import time
import sys

def keep_server_running():
    """إبقاء الخادم يعمل"""
    while True:
        try:
            print("🔄 بدء تشغيل الخادم...")
            subprocess.run([sys.executable, "restart_platform.py"])
        except KeyboardInterrupt:
            print("\\n✅ تم إيقاف الخادم بواسطة المستخدم")
            break
        except Exception as e:
            print(f"❌ خطأ: {e}")
            print("⏳ إعادة المحاولة خلال 10 ثوان...")
            time.sleep(10)

if __name__ == "__main__":
    keep_server_running()
'''
    
    with open("auto_restart.py", "w", encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ تم إنشاء سكريبت إعادة التشغيل التلقائي")

def main():
    """الدالة الرئيسية"""
    print("🔄 إعادة تشغيل منصة المسابقات الرياضية")
    print("="*50)
    
    # إنشاء سكريبت إعادة التشغيل التلقائي
    create_auto_restart_script()
    
    # الحصول على رابط جديد
    new_url = get_new_ngrok_url()
    
    if new_url:
        print("\n🎯 المنصة جاهزة مع الرابط الجديد!")
        print("📋 شارك الرابط الجديد مع المشاركين")
        print("⏹️ اضغط Ctrl+C لإيقاف الخادم")
        
        # تشغيل الخادم
        start_django_server()
    else:
        print("\n❌ فشل في إنشاء رابط جديد")
        print("💡 جرب تشغيل الأمر مرة أخرى")

if __name__ == "__main__":
    main()
