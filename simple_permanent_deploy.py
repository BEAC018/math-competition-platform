#!/usr/bin/env python3
"""
🚀 نشر دائم مبسط مع ngrok
Simple permanent deployment with ngrok
"""

import subprocess
import sys
import time
import threading
import os
import json

class SimplePermanentPlatform:
    def __init__(self):
        self.ngrok_process = None
        self.django_process = None
        self.running = True
        self.current_url = None
    
    def start_django(self):
        """تشغيل Django"""
        print("🚀 تشغيل خادم Django...")
        
        try:
            # إعداد Django
            subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
            subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
            
            # تشغيل الخادم
            self.django_process = subprocess.Popen([
                sys.executable, "manage.py", "runserver", "0.0.0.0:8000"
            ])
            
            print("✅ Django يعمل على المنفذ 8000")
            time.sleep(3)  # انتظار حتى يبدأ Django
            return True
            
        except Exception as e:
            print(f"❌ خطأ في تشغيل Django: {e}")
            return False
    
    def start_ngrok(self):
        """تشغيل ngrok"""
        print("🌐 تشغيل ngrok...")
        
        try:
            # إغلاق أي عمليات ngrok سابقة
            self.kill_ngrok()
            time.sleep(2)
            
            # تشغيل ngrok
            self.ngrok_process = subprocess.Popen([
                'ngrok', 'http', '8000'
            ])
            
            print("✅ ngrok يعمل")
            time.sleep(5)  # انتظار حتى يبدأ ngrok
            
            # محاولة الحصول على الرابط
            url = self.get_ngrok_url()
            if url:
                self.current_url = url
                print(f"🌐 الرابط: {url}")
                self.save_info()
                return True
            else:
                print("⚠️ لم يتمكن من الحصول على الرابط تلقائياً")
                print("📋 تحقق من نافذة ngrok للحصول على الرابط")
                return True
                
        except Exception as e:
            print(f"❌ خطأ في تشغيل ngrok: {e}")
            return False
    
    def get_ngrok_url(self):
        """محاولة الحصول على رابط ngrok"""
        try:
            import requests
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                data = response.json()
                tunnels = data.get('tunnels', [])
                
                for tunnel in tunnels:
                    if tunnel.get('proto') == 'https':
                        return tunnel.get('public_url')
                
                if tunnels:
                    return tunnels[0].get('public_url')
            
            return None
            
        except:
            return None
    
    def kill_ngrok(self):
        """إغلاق عمليات ngrok"""
        try:
            if self.ngrok_process:
                self.ngrok_process.terminate()
                self.ngrok_process = None
            
            if os.name == 'nt':  # Windows
                subprocess.run(['taskkill', '/f', '/im', 'ngrok.exe'], 
                             capture_output=True, text=True)
            else:  # Linux/Mac
                subprocess.run(['pkill', '-f', 'ngrok'], 
                             capture_output=True, text=True)
                             
        except:
            pass
    
    def save_info(self):
        """حفظ معلومات المنصة"""
        if self.current_url:
            info = f"""🌐 منصة المسابقات الرياضية - تعمل الآن!
{"="*50}

🔗 الروابط:
├── الرابط الرئيسي: {self.current_url}
├── رابط التلاميذ: {self.current_url}/student/login/
├── رابط الأساتذة: {self.current_url}/accounts/login/
└── رمز الدخول: ben25

📱 رسالة للمشاركة:
{"-"*30}
🎯 منصة المسابقات الرياضية

🌐 الرابط: {self.current_url}/student/login/
🔑 رمز الدخول: ben25

📝 الخطوات:
1. انقر الرابط
2. اكتب اسمك
3. اكتب الرمز: ben25
4. اختر مستواك
5. ابدأ المسابقة!

🎮 استمتعوا! 🚀

📊 الحالة: تعمل
⏰ التحديث: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""

            with open("PLATFORM_INFO.txt", "w", encoding='utf-8') as f:
                f.write(info)
            
            print("📄 تم حفظ المعلومات في PLATFORM_INFO.txt")
    
    def monitor(self):
        """مراقبة بسيطة"""
        while self.running:
            try:
                # فحص Django
                if self.django_process and self.django_process.poll() is not None:
                    print("⚠️ Django توقف، إعادة تشغيل...")
                    self.start_django()
                
                # فحص ngrok
                if self.ngrok_process and self.ngrok_process.poll() is not None:
                    print("⚠️ ngrok توقف، إعادة تشغيل...")
                    self.start_ngrok()
                
                time.sleep(30)  # فحص كل 30 ثانية
                
            except Exception as e:
                print(f"⚠️ خطأ في المراقبة: {e}")
                time.sleep(10)
    
    def cleanup(self):
        """تنظيف"""
        print("\n🛑 إيقاف المنصة...")
        self.running = False
        
        if self.django_process:
            self.django_process.terminate()
            print("✅ تم إيقاف Django")
        
        self.kill_ngrok()
        print("✅ تم إيقاف ngrok")
        print("✅ تم إيقاف المنصة")
    
    def run(self):
        """تشغيل المنصة"""
        print("🎯 بدء تشغيل منصة المسابقات الرياضية - النشر الدائم")
        print("="*60)
        
        try:
            # تشغيل Django
            if not self.start_django():
                return
            
            # تشغيل ngrok
            if not self.start_ngrok():
                return
            
            print("\n" + "="*60)
            print("🎉 المنصة تعمل الآن!")
            print("="*60)
            if self.current_url:
                print(f"🌐 الرابط: {self.current_url}")
                print(f"👥 للتلاميذ: {self.current_url}/student/login/")
                print(f"🔑 رمز الدخول: ben25")
            else:
                print("📋 تحقق من نافذة ngrok للحصول على الرابط")
            print("📄 تحقق من ملف PLATFORM_INFO.txt للتفاصيل")
            print("⏹️ اضغط Ctrl+C لإيقاف المنصة")
            print("="*60)
            
            # بدء المراقبة
            monitor_thread = threading.Thread(target=self.monitor)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            # إبقاء البرنامج يعمل
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 تم طلب إيقاف المنصة...")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        finally:
            self.cleanup()

def main():
    """الدالة الرئيسية"""
    platform = SimplePermanentPlatform()
    platform.run()

if __name__ == "__main__":
    main()
