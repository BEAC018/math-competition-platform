#!/usr/bin/env python3
"""
🚀 نشر دائم لمنصة المسابقات الرياضية مع ngrok
Permanent deployment for Math Competition Platform with ngrok
"""

import subprocess
import sys
import time
import threading
import os
import json
import signal
import requests
from pathlib import Path

class PermanentMathPlatform:
    def __init__(self):
        self.ngrok_process = None
        self.django_process = None
        self.running = True
        self.current_url = None
        self.restart_count = 0
        self.max_restarts = 10
    
    def setup_ngrok_auth(self):
        """إعداد مصادقة ngrok"""
        print("🔐 إعداد مصادقة ngrok...")
        
        # محاولة الحصول على التوكن من متغيرات البيئة
        auth_token = os.environ.get('NGROK_AUTHTOKEN')
        
        if not auth_token:
            print("⚠️ لم يتم العثور على NGROK_AUTHTOKEN في متغيرات البيئة")
            print("📋 للحصول على توكن مجاني:")
            print("1. اذهب إلى https://ngrok.com/signup")
            print("2. أنشئ حساب مجاني")
            print("3. انسخ التوكن من https://dashboard.ngrok.com/get-started/your-authtoken")
            
            # محاولة استخدام ngrok بدون توكن (محدود)
            print("🔄 محاولة التشغيل بدون توكن (محدود)...")
            return True
        
        try:
            # إعداد التوكن
            result = subprocess.run([
                'ngrok', 'config', 'add-authtoken', auth_token
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ تم إعداد توكن ngrok بنجاح")
                return True
            else:
                print(f"❌ فشل في إعداد التوكن: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في إعداد ngrok: {e}")
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
                'ngrok', 'http', '8000', '--log=stdout'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # انتظار حتى يبدأ ngrok
            time.sleep(5)
            
            # الحصول على الرابط
            url = self.get_ngrok_url()
            if url:
                self.current_url = url
                print(f"✅ ngrok يعمل على: {url}")
                self.save_current_info()
                return True
            else:
                print("❌ فشل في الحصول على رابط ngrok")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في تشغيل ngrok: {e}")
            return False
    
    def get_ngrok_url(self):
        """الحصول على رابط ngrok من API"""
        try:
            # محاولة الاتصال بـ ngrok API
            response = requests.get('http://localhost:4040/api/tunnels', timeout=10)
            if response.status_code == 200:
                data = response.json()
                tunnels = data.get('tunnels', [])
                
                for tunnel in tunnels:
                    if tunnel.get('proto') == 'https':
                        return tunnel.get('public_url')
                
                # إذا لم نجد https، نأخذ أول رابط متاح
                if tunnels:
                    return tunnels[0].get('public_url')
            
            return None
            
        except Exception as e:
            print(f"⚠️ لم يتمكن من الحصول على رابط ngrok: {e}")
            return None
    
    def kill_ngrok(self):
        """إغلاق عمليات ngrok"""
        try:
            if self.ngrok_process:
                self.ngrok_process.terminate()
                self.ngrok_process = None
            
            # إغلاق عمليات ngrok أخرى
            if os.name == 'nt':  # Windows
                subprocess.run(['taskkill', '/f', '/im', 'ngrok.exe'], 
                             capture_output=True, text=True)
            else:  # Linux/Mac
                subprocess.run(['pkill', '-f', 'ngrok'], 
                             capture_output=True, text=True)
                             
        except Exception as e:
            print(f"⚠️ خطأ في إغلاق ngrok: {e}")
    
    def start_django(self):
        """تشغيل Django"""
        print("🚀 تشغيل خادم Django...")
        
        try:
            # إعداد Django أولاً
            subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
            subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
            
            # تشغيل الخادم
            self.django_process = subprocess.Popen([
                sys.executable, "manage.py", "runserver", "0.0.0.0:8000"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            print("✅ Django يعمل على المنفذ 8000")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في تشغيل Django: {e}")
            return False
    
    def save_current_info(self):
        """حفظ معلومات الرابط الحالي"""
        if not self.current_url:
            return
        
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # حفظ في ملف نصي
        info_content = f"""🌐 منصة المسابقات الرياضية - معلومات النشر الدائم
{"="*60}

📅 تاريخ التحديث: {current_time}
🔄 عدد إعادات التشغيل: {self.restart_count}

🌐 الروابط الحالية:
├── الرابط الرئيسي: {self.current_url}
├── رابط التلاميذ: {self.current_url}/student/login/
├── رابط الأساتذة: {self.current_url}/accounts/login/
└── رمز الدخول: ben25

📱 رسالة للمشاركة:
{"-"*30}
🎯 منصة المسابقات الرياضية

🌐 الرابط: {self.current_url}/student/login/
🔑 رمز الدخول: ben25

📝 خطوات الدخول:
1️⃣ انقر على الرابط أعلاه
2️⃣ اكتب اسمك الكامل
3️⃣ اكتب رمز الدخول: ben25
4️⃣ اختر مستواك الدراسي (1-9)
5️⃣ ابدأ المسابقة!

🎮 استمتعوا بالتعلم! 🚀

📊 معلومات تقنية:
├── حالة ngrok: يعمل
├── حالة Django: يعمل
├── المنفذ المحلي: 8000
└── وضع المراقبة: مفعل
"""

        with open("PERMANENT_DEPLOYMENT_INFO.txt", "w", encoding='utf-8') as f:
            f.write(info_content)
        
        # حفظ JSON للبرمجة
        json_info = {
            "url": self.current_url,
            "student_url": f"{self.current_url}/student/login/",
            "teacher_url": f"{self.current_url}/accounts/login/",
            "access_code": "ben25",
            "last_update": current_time,
            "restart_count": self.restart_count,
            "status": "running"
        }
        
        with open("deployment_status.json", "w", encoding='utf-8') as f:
            json.dump(json_info, f, indent=2, ensure_ascii=False)
        
        print("📄 تم حفظ معلومات النشر في PERMANENT_DEPLOYMENT_INFO.txt")
    
    def monitor_services(self):
        """مراقبة الخدمات وإعادة تشغيلها عند الحاجة"""
        print("👁️ بدء مراقبة الخدمات...")
        
        while self.running and self.restart_count < self.max_restarts:
            try:
                # فحص Django
                if self.django_process and self.django_process.poll() is not None:
                    print("⚠️ Django توقف، إعادة تشغيل...")
                    self.start_django()
                    self.restart_count += 1
                
                # فحص ngrok
                if self.ngrok_process and self.ngrok_process.poll() is not None:
                    print("⚠️ ngrok توقف، إعادة تشغيل...")
                    self.start_ngrok()
                    self.restart_count += 1
                
                # فحص الرابط
                if self.current_url:
                    try:
                        response = requests.get(self.current_url, timeout=10)
                        if response.status_code != 200:
                            print("⚠️ الرابط لا يستجيب، إعادة تشغيل ngrok...")
                            self.start_ngrok()
                            self.restart_count += 1
                    except:
                        print("⚠️ فشل في الوصول للرابط، إعادة تشغيل ngrok...")
                        self.start_ngrok()
                        self.restart_count += 1
                
                # تحديث المعلومات
                self.save_current_info()
                
                # انتظار قبل الفحص التالي
                time.sleep(30)
                
            except Exception as e:
                print(f"❌ خطأ في المراقبة: {e}")
                time.sleep(10)
        
        if self.restart_count >= self.max_restarts:
            print(f"⚠️ تم الوصول للحد الأقصى من إعادات التشغيل ({self.max_restarts})")
    
    def display_info(self):
        """عرض معلومات المنصة"""
        if self.current_url:
            print("\n" + "="*60)
            print("🎉 منصة المسابقات الرياضية تعمل بنجاح!")
            print("="*60)
            print(f"🌐 الرابط الرئيسي: {self.current_url}")
            print(f"👥 رابط التلاميذ: {self.current_url}/student/login/")
            print(f"👨‍🏫 رابط الأساتذة: {self.current_url}/accounts/login/")
            print(f"🔑 رمز دخول التلاميذ: ben25")
            print("="*60)
            print("📋 المنصة تعمل الآن بشكل دائم!")
            print("📄 تحقق من ملف PERMANENT_DEPLOYMENT_INFO.txt للتفاصيل")
            print("⏹️ اضغط Ctrl+C لإيقاف المنصة")
            print("="*60)
    
    def cleanup(self):
        """تنظيف الموارد"""
        print("\n🛑 إيقاف المنصة...")
        self.running = False
        
        if self.django_process:
            self.django_process.terminate()
            print("✅ تم إيقاف Django")
        
        self.kill_ngrok()
        print("✅ تم إيقاف ngrok")
        
        # تحديث حالة النشر
        try:
            with open("deployment_status.json", "r", encoding='utf-8') as f:
                status = json.load(f)
            status["status"] = "stopped"
            status["last_update"] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            with open("deployment_status.json", "w", encoding='utf-8') as f:
                json.dump(status, f, indent=2, ensure_ascii=False)
        except:
            pass
        
        print("✅ تم إيقاف المنصة بنجاح")
    
    def run(self):
        """تشغيل المنصة الدائمة"""
        print("🎯 بدء تشغيل منصة المسابقات الرياضية - النشر الدائم")
        print("="*65)
        
        try:
            # إعداد ngrok
            if not self.setup_ngrok_auth():
                print("⚠️ تحذير: ngrok قد يعمل بقيود")
            
            # تشغيل Django
            if not self.start_django():
                print("❌ فشل في تشغيل Django")
                return
            
            # تشغيل ngrok
            if not self.start_ngrok():
                print("❌ فشل في تشغيل ngrok")
                return
            
            # عرض المعلومات
            self.display_info()
            
            # بدء المراقبة
            monitor_thread = threading.Thread(target=self.monitor_services)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            # إبقاء البرنامج يعمل
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 تم طلب إيقاف المنصة...")
        except Exception as e:
            print(f"❌ خطأ عام: {e}")
        finally:
            self.cleanup()

def main():
    """الدالة الرئيسية"""
    platform = PermanentMathPlatform()
    
    # معالج الإشارات للإيقاف الآمن
    def signal_handler(sig, frame):
        platform.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    platform.run()

if __name__ == "__main__":
    main()
