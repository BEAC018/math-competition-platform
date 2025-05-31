#!/usr/bin/env python3
"""
🔧 إصلاح وإعادة تشغيل المنصة
Fix and restart platform
"""

import subprocess
import sys
import time
import os
import signal

def kill_all_ngrok():
    """إغلاق جميع عمليات ngrok"""
    print("🔄 إغلاق جميع عمليات ngrok...")
    
    try:
        # إغلاق ngrok بالطريقة البرمجية
        from pyngrok import ngrok
        ngrok.kill()
        print("✅ تم إغلاق ngrok بالطريقة البرمجية")
    except:
        pass
    
    try:
        # إغلاق ngrok بالأوامر
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/f', '/im', 'ngrok.exe'], 
                         capture_output=True, text=True)
        else:  # Linux/Mac
            subprocess.run(['pkill', '-f', 'ngrok'], 
                         capture_output=True, text=True)
        print("✅ تم إغلاق عمليات ngrok")
    except:
        pass
    
    # انتظار قليل
    time.sleep(3)

def start_fresh_ngrok():
    """بدء ngrok جديد"""
    try:
        from pyngrok import ngrok
        
        print("🌐 إنشاء نفق جديد...")
        public_url = ngrok.connect(8000)
        
        # استخراج الرابط النظيف
        clean_url = str(public_url).split('"')[1]
        
        print("\n" + "="*60)
        print("🎉 تم إنشاء الرابط الجديد بنجاح!")
        print("="*60)
        print(f"🌐 الرابط الجديد: {clean_url}")
        print(f"👥 رابط التلاميذ: {clean_url}/student/login/")
        print(f"👨‍🏫 رابط الأساتذة: {clean_url}/accounts/login/")
        print(f"🔑 رمز دخول التلاميذ: ben25")
        print("="*60)
        
        # حفظ الرابط الجديد
        save_new_urls(clean_url)
        
        return clean_url
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء ngrok: {e}")
        return None

def save_new_urls(clean_url):
    """حفظ الروابط الجديدة"""
    
    # حفظ في ملف نصي
    with open("LATEST_URL.txt", "w", encoding='utf-8') as f:
        f.write(f"🌐 الرابط الحالي للمنصة\n")
        f.write("="*30 + "\n\n")
        f.write(f"الرابط الرئيسي: {clean_url}\n")
        f.write(f"رابط التلاميذ: {clean_url}/student/login/\n")
        f.write(f"رابط الأساتذة: {clean_url}/accounts/login/\n")
        f.write(f"رمز الدخول: ben25\n")
        f.write(f"تاريخ التحديث: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # رسالة WhatsApp جديدة
    whatsapp_msg = f"""🎯 منصة المسابقات الرياضية - رابط محدث

🌐 الرابط الجديد:
{clean_url}/student/login/

🔑 رمز الدخول: ben25

📝 خطوات الدخول:
1️⃣ انقر على الرابط أعلاه
2️⃣ اكتب اسمك الكامل
3️⃣ اكتب رمز الدخول: ben25
4️⃣ اختر مستواك الدراسي (1-9)
5️⃣ ابدأ المسابقة!

🎮 استمتعوا بالتعلم! 🚀

ملاحظة: هذا رابط محدث، استخدموه بدلاً من الرابط السابق"""

    with open("UPDATED_SHARE_MESSAGE.txt", "w", encoding='utf-8') as f:
        f.write(whatsapp_msg)
    
    print("📄 تم حفظ الروابط في LATEST_URL.txt")
    print("📱 تم حفظ رسالة المشاركة في UPDATED_SHARE_MESSAGE.txt")

def start_django():
    """تشغيل Django"""
    print("🚀 تشغيل خادم Django...")
    try:
        subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
    except KeyboardInterrupt:
        print("\n✅ تم إيقاف الخادم")

def main():
    """الدالة الرئيسية"""
    print("🔧 إصلاح وإعادة تشغيل منصة المسابقات الرياضية")
    print("="*55)
    
    # إغلاق جميع عمليات ngrok
    kill_all_ngrok()
    
    # بدء ngrok جديد
    new_url = start_fresh_ngrok()
    
    if new_url:
        print("\n🎯 المنصة جاهزة مع الرابط الجديد!")
        print("📋 شارك الرابط الجديد مع المشاركين")
        print("📁 تحقق من ملف UPDATED_SHARE_MESSAGE.txt للرسالة الجديدة")
        print("⏹️ اضغط Ctrl+C لإيقاف الخادم")
        
        # تشغيل Django
        start_django()
    else:
        print("\n❌ فشل في إنشاء رابط جديد")
        print("💡 تحقق من اتصال الإنترنت وحاول مرة أخرى")

if __name__ == "__main__":
    main()
