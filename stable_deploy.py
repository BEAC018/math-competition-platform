#!/usr/bin/env python3
"""
🚀 نشر مستقر مع إعادة تشغيل تلقائي
Stable deployment with auto-restart
"""

import subprocess
import sys
import time
import threading
import os
import signal

class StablePlatform:
    def __init__(self):
        self.ngrok_url = None
        self.django_process = None
        self.running = True
    
    def kill_all_ngrok(self):
        """إغلاق جميع عمليات ngrok"""
        print("🔄 إغلاق عمليات ngrok السابقة...")
        
        try:
            from pyngrok import ngrok
            ngrok.kill()
            print("✅ تم إغلاق ngrok")
        except:
            pass
        
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(['taskkill', '/f', '/im', 'ngrok.exe'], 
                             capture_output=True, text=True)
            else:  # Linux/Mac
                subprocess.run(['pkill', '-f', 'ngrok'], 
                             capture_output=True, text=True)
        except:
            pass
        
        time.sleep(2)
    
    def create_ngrok_tunnel(self):
        """إنشاء نفق ngrok جديد"""
        try:
            from pyngrok import ngrok
            
            print("🌐 إنشاء نفق جديد...")
            public_url = ngrok.connect(8000)
            
            # استخراج الرابط النظيف
            clean_url = str(public_url).split('"')[1]
            self.ngrok_url = clean_url
            
            print("\n" + "="*60)
            print("🎉 تم إنشاء رابط جديد بنجاح!")
            print("="*60)
            print(f"🌐 الرابط الجديد: {clean_url}")
            print(f"👥 رابط التلاميذ: {clean_url}/student/login/")
            print(f"👨‍🏫 رابط الأساتذة: {clean_url}/accounts/login/")
            print(f"🔑 رمز دخول التلاميذ: ben25")
            print("="*60)
            
            # حفظ الرابط
            self.save_current_url(clean_url)
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء ngrok: {e}")
            return False
    
    def save_current_url(self, url):
        """حفظ الرابط الحالي"""
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # حفظ في ملف نصي
        with open("CURRENT_PLATFORM_URL.txt", "w", encoding='utf-8') as f:
            f.write(f"🌐 منصة المسابقات الرياضية - الرابط الحالي\n")
            f.write("="*50 + "\n\n")
            f.write(f"الرابط الرئيسي: {url}\n")
            f.write(f"رابط التلاميذ: {url}/student/login/\n")
            f.write(f"رابط الأساتذة: {url}/accounts/login/\n")
            f.write(f"رمز الدخول: ben25\n")
            f.write(f"آخر تحديث: {current_time}\n\n")
            f.write("📱 رسالة للمشاركة:\n")
            f.write("-"*30 + "\n")
            f.write(f"🎯 منصة المسابقات الرياضية\n\n")
            f.write(f"🌐 الرابط: {url}/student/login/\n")
            f.write(f"🔑 رمز الدخول: ben25\n\n")
            f.write("📝 الخطوات:\n")
            f.write("1. انقر الرابط\n")
            f.write("2. اكتب اسمك\n")
            f.write("3. اكتب الرمز: ben25\n")
            f.write("4. اختر مستواك\n")
            f.write("5. ابدأ المسابقة!\n\n")
            f.write("🎮 استمتعوا! 🚀\n")
        
        print("📄 تم حفظ الرابط في CURRENT_PLATFORM_URL.txt")
    
    def start_django(self):
        """تشغيل Django"""
        print("🚀 تشغيل خادم Django...")
        try:
            self.django_process = subprocess.Popen([
                sys.executable, "manage.py", "runserver", "0.0.0.0:8000"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            return True
        except Exception as e:
            print(f"❌ خطأ في تشغيل Django: {e}")
            return False
    
    def monitor_django(self):
        """مراقبة Django وإعادة تشغيله عند الحاجة"""
        while self.running:
            if self.django_process and self.django_process.poll() is not None:
                print("⚠️ Django توقف، إعادة تشغيل...")
                self.start_django()
            time.sleep(5)
    
    def run(self):
        """تشغيل المنصة"""
        print("🎯 بدء تشغيل المنصة المستقرة...")
        
        # إغلاق العمليات السابقة
        self.kill_all_ngrok()
        
        # إنشاء نفق جديد
        if not self.create_ngrok_tunnel():
            print("❌ فشل في إنشاء النفق")
            return
        
        # تشغيل Django
        if not self.start_django():
            print("❌ فشل في تشغيل Django")
            return
        
        # بدء المراقبة
        monitor_thread = threading.Thread(target=self.monitor_django)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        print("\n🎯 المنصة تعمل الآن!")
        print("📋 تحقق من ملف CURRENT_PLATFORM_URL.txt للرابط الحالي")
        print("⏹️ اضغط Ctrl+C لإيقاف المنصة")
        
        try:
            # إبقاء البرنامج يعمل
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 إيقاف المنصة...")
            self.stop()
    
    def stop(self):
        """إيقاف المنصة"""
        self.running = False
        
        if self.django_process:
            self.django_process.terminate()
            print("✅ تم إيقاف Django")
        
        try:
            from pyngrok import ngrok
            ngrok.kill()
            print("✅ تم إيقاف ngrok")
        except:
            pass
        
        print("✅ تم إيقاف المنصة بنجاح")

def create_quick_start_script():
    """إنشاء سكريبت بدء سريع"""
    script_content = '''#!/usr/bin/env python3
"""
🚀 بدء سريع للمنصة
Quick start for platform
"""

import subprocess
import sys

def main():
    print("🚀 بدء تشغيل منصة المسابقات الرياضية...")
    try:
        subprocess.run([sys.executable, "stable_deploy.py"])
    except KeyboardInterrupt:
        print("\\n✅ تم إيقاف المنصة")

if __name__ == "__main__":
    main()
'''
    
    with open("start_platform.py", "w", encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ تم إنشاء سكريبت البدء السريع: start_platform.py")

def main():
    """الدالة الرئيسية"""
    print("🎯 منصة المسابقات الرياضية - النشر المستقر")
    print("="*55)
    
    # إنشاء سكريبت البدء السريع
    create_quick_start_script()
    
    # تشغيل المنصة
    platform = StablePlatform()
    platform.run()

if __name__ == "__main__":
    main()
