#!/usr/bin/env python3
"""
🔍 نظام مراقبة متقدم لضمان استمرارية المنصة
Advanced monitoring system for platform continuity
"""

import subprocess
import sys
import time
import threading
import os
import json
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import logging

class AdvancedMonitor:
    def __init__(self):
        self.current_url = None
        self.django_process = None
        self.ngrok_process = None
        self.running = True
        self.restart_count = 0
        self.last_restart = None
        self.uptime_start = datetime.now()
        
        # إعداد التسجيل
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('platform_monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_system_resources(self):
        """فحص موارد النظام"""
        try:
            import psutil
            
            # فحص المعالج
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # فحص الذاكرة
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # فحص القرص
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # تسجيل الحالة
            self.logger.info(f"موارد النظام - CPU: {cpu_percent}%, RAM: {memory_percent}%, Disk: {disk_percent}%")
            
            # تحذيرات
            if cpu_percent > 80:
                self.logger.warning(f"استخدام المعالج مرتفع: {cpu_percent}%")
            
            if memory_percent > 80:
                self.logger.warning(f"استخدام الذاكرة مرتفع: {memory_percent}%")
            
            if disk_percent > 90:
                self.logger.error(f"مساحة القرص منخفضة: {disk_percent}%")
            
            return {
                'cpu': cpu_percent,
                'memory': memory_percent,
                'disk': disk_percent,
                'status': 'healthy' if all(x < 80 for x in [cpu_percent, memory_percent]) else 'warning'
            }
            
        except ImportError:
            self.logger.warning("psutil غير مثبت - تثبيت للحصول على مراقبة أفضل")
            return {'status': 'unknown'}
        except Exception as e:
            self.logger.error(f"خطأ في فحص موارد النظام: {e}")
            return {'status': 'error'}
    
    def check_internet_connection(self):
        """فحص اتصال الإنترنت"""
        try:
            # فحص عدة خوادم
            test_urls = [
                'https://www.google.com',
                'https://www.cloudflare.com',
                'https://www.github.com'
            ]
            
            for url in test_urls:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        self.logger.info("اتصال الإنترنت متاح")
                        return True
                except:
                    continue
            
            self.logger.error("لا يوجد اتصال بالإنترنت")
            return False
            
        except Exception as e:
            self.logger.error(f"خطأ في فحص الإنترنت: {e}")
            return False
    
    def check_ngrok_status(self):
        """فحص حالة ngrok"""
        try:
            # فحص API ngrok
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                data = response.json()
                tunnels = data.get('tunnels', [])
                
                if tunnels:
                    for tunnel in tunnels:
                        if tunnel.get('proto') == 'https':
                            url = tunnel.get('public_url')
                            if url != self.current_url:
                                self.current_url = url
                                self.logger.info(f"رابط ngrok جديد: {url}")
                                self.save_current_status()
                            return True
                
                self.logger.warning("لا توجد أنفاق ngrok نشطة")
                return False
            else:
                self.logger.error(f"ngrok API غير متاح: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"خطأ في فحص ngrok: {e}")
            return False
    
    def check_django_status(self):
        """فحص حالة Django"""
        try:
            if self.django_process:
                if self.django_process.poll() is None:
                    # فحص الاستجابة
                    response = requests.get('http://localhost:8000', timeout=5)
                    if response.status_code in [200, 302, 404]:  # أي استجابة تعني أن Django يعمل
                        return True
                    else:
                        self.logger.warning(f"Django يستجيب بكود: {response.status_code}")
                        return False
                else:
                    self.logger.error("عملية Django متوقفة")
                    return False
            else:
                self.logger.error("عملية Django غير موجودة")
                return False
                
        except Exception as e:
            self.logger.error(f"خطأ في فحص Django: {e}")
            return False
    
    def restart_django(self):
        """إعادة تشغيل Django"""
        try:
            self.logger.info("إعادة تشغيل Django...")
            
            # إيقاف العملية الحالية
            if self.django_process:
                self.django_process.terminate()
                time.sleep(2)
            
            # تشغيل جديد
            self.django_process = subprocess.Popen([
                sys.executable, "manage.py", "runserver", "0.0.0.0:8000"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            time.sleep(5)  # انتظار البدء
            
            if self.check_django_status():
                self.logger.info("تم إعادة تشغيل Django بنجاح")
                return True
            else:
                self.logger.error("فشل في إعادة تشغيل Django")
                return False
                
        except Exception as e:
            self.logger.error(f"خطأ في إعادة تشغيل Django: {e}")
            return False
    
    def restart_ngrok(self):
        """إعادة تشغيل ngrok"""
        try:
            self.logger.info("إعادة تشغيل ngrok...")
            
            # إيقاف العملية الحالية
            if self.ngrok_process:
                self.ngrok_process.terminate()
                time.sleep(2)
            
            # إغلاق أي عمليات ngrok أخرى
            if os.name == 'nt':
                subprocess.run(['taskkill', '/f', '/im', 'ngrok.exe'], 
                             capture_output=True, text=True)
            else:
                subprocess.run(['pkill', '-f', 'ngrok'], 
                             capture_output=True, text=True)
            
            time.sleep(3)
            
            # تشغيل جديد
            self.ngrok_process = subprocess.Popen([
                'ngrok', 'http', '8000'
            ])
            
            time.sleep(10)  # انتظار البدء
            
            if self.check_ngrok_status():
                self.logger.info("تم إعادة تشغيل ngrok بنجاح")
                self.restart_count += 1
                self.last_restart = datetime.now()
                return True
            else:
                self.logger.error("فشل في إعادة تشغيل ngrok")
                return False
                
        except Exception as e:
            self.logger.error(f"خطأ في إعادة تشغيل ngrok: {e}")
            return False
    
    def save_current_status(self):
        """حفظ الحالة الحالية"""
        try:
            status = {
                'current_url': self.current_url,
                'student_url': f"{self.current_url}/student/login/" if self.current_url else None,
                'teacher_url': f"{self.current_url}/accounts/login/" if self.current_url else None,
                'access_code': 'ben25',
                'last_update': datetime.now().isoformat(),
                'restart_count': self.restart_count,
                'last_restart': self.last_restart.isoformat() if self.last_restart else None,
                'uptime': str(datetime.now() - self.uptime_start),
                'status': 'running'
            }
            
            # حفظ JSON
            with open('platform_status.json', 'w', encoding='utf-8') as f:
                json.dump(status, f, indent=2, ensure_ascii=False)
            
            # حفظ ملف نصي للمشاركة
            if self.current_url:
                share_message = f"""🎯 منصة المسابقات الرياضية - محدث تلقائياً

🌐 الرابط الحالي: {self.current_url}/student/login/
🔑 رمز الدخول: ben25

📊 إحصائيات:
├── عدد إعادات التشغيل: {self.restart_count}
├── آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
├── مدة التشغيل: {datetime.now() - self.uptime_start}
└── الحالة: يعمل ✅

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
"""
                
                with open('CURRENT_PLATFORM_STATUS.txt', 'w', encoding='utf-8') as f:
                    f.write(share_message)
            
        except Exception as e:
            self.logger.error(f"خطأ في حفظ الحالة: {e}")
    
    def monitor_loop(self):
        """حلقة المراقبة الرئيسية"""
        self.logger.info("بدء نظام المراقبة المتقدم")
        
        while self.running:
            try:
                # فحص موارد النظام
                system_status = self.check_system_resources()
                
                # فحص الإنترنت
                internet_ok = self.check_internet_connection()
                
                if not internet_ok:
                    self.logger.error("لا يوجد اتصال بالإنترنت - انتظار...")
                    time.sleep(30)
                    continue
                
                # فحص Django
                django_ok = self.check_django_status()
                if not django_ok:
                    self.logger.warning("Django لا يعمل - محاولة إعادة التشغيل...")
                    self.restart_django()
                
                # فحص ngrok
                ngrok_ok = self.check_ngrok_status()
                if not ngrok_ok:
                    self.logger.warning("ngrok لا يعمل - محاولة إعادة التشغيل...")
                    self.restart_ngrok()
                
                # حفظ الحالة
                self.save_current_status()
                
                # انتظار قبل الفحص التالي
                time.sleep(30)
                
            except KeyboardInterrupt:
                self.logger.info("تم طلب إيقاف المراقبة")
                break
            except Exception as e:
                self.logger.error(f"خطأ في حلقة المراقبة: {e}")
                time.sleep(10)
        
        self.logger.info("تم إيقاف نظام المراقبة")
    
    def start_monitoring(self):
        """بدء المراقبة"""
        monitor_thread = threading.Thread(target=self.monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        return monitor_thread

def main():
    """الدالة الرئيسية"""
    monitor = AdvancedMonitor()
    
    print("🔍 بدء نظام المراقبة المتقدم...")
    print("📊 سيتم فحص الحالة كل 30 ثانية")
    print("📄 تحقق من platform_monitor.log للتفاصيل")
    print("⏹️ اضغط Ctrl+C لإيقاف المراقبة")
    
    try:
        monitor_thread = monitor.start_monitoring()
        
        # إبقاء البرنامج يعمل
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 إيقاف نظام المراقبة...")
        monitor.running = False

if __name__ == "__main__":
    main()
