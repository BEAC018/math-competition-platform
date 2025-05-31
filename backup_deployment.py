#!/usr/bin/env python3
"""
🔄 نظام النسخ الاحتياطية للمنصة
Backup deployment system
"""

import subprocess
import sys
import time
import os
import json
import shutil
from datetime import datetime

class BackupDeployment:
    def __init__(self):
        self.backup_methods = {
            'cloudflare': self.setup_cloudflare_tunnel,
            'localtunnel': self.setup_localtunnel,
            'railway': self.deploy_to_railway,
            'render': self.deploy_to_render
        }
        self.active_backups = []
    
    def setup_cloudflare_tunnel(self):
        """إعداد Cloudflare Tunnel كبديل مجاني"""
        print("🌐 إعداد Cloudflare Tunnel...")
        
        try:
            # تحقق من وجود cloudflared
            result = subprocess.run(['cloudflared', '--version'], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print("📦 تثبيت Cloudflare Tunnel...")
                # تعليمات التثبيت
                print("💡 لتثبيت Cloudflare Tunnel:")
                print("1. اذهب إلى: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/")
                print("2. حمل cloudflared")
                print("3. شغل: cloudflared tunnel login")
                print("4. شغل: cloudflared tunnel create math-platform")
                print("5. شغل: cloudflared tunnel route dns math-platform math-platform.your-domain.com")
                return False
            
            # تشغيل النفق
            tunnel_process = subprocess.Popen([
                'cloudflared', 'tunnel', 'run', 'math-platform'
            ])
            
            self.active_backups.append({
                'name': 'cloudflare',
                'process': tunnel_process,
                'url': 'https://math-platform.your-domain.com'
            })
            
            print("✅ Cloudflare Tunnel يعمل")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في Cloudflare Tunnel: {e}")
            return False
    
    def setup_localtunnel(self):
        """إعداد LocalTunnel كبديل"""
        print("🔗 إعداد LocalTunnel...")
        
        try:
            # تثبيت localtunnel
            subprocess.run(['npm', 'install', '-g', 'localtunnel'], check=True)
            
            # تشغيل النفق
            tunnel_process = subprocess.Popen([
                'lt', '--port', '8000', '--subdomain', 'math-competition'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            time.sleep(5)
            
            self.active_backups.append({
                'name': 'localtunnel',
                'process': tunnel_process,
                'url': 'https://math-competition.loca.lt'
            })
            
            print("✅ LocalTunnel يعمل على: https://math-competition.loca.lt")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في LocalTunnel: {e}")
            return False
    
    def deploy_to_railway(self):
        """نشر على Railway"""
        print("🚂 إعداد النشر على Railway...")
        
        try:
            # إنشاء ملفات Railway
            railway_config = {
                "build": {
                    "builder": "NIXPACKS"
                },
                "deploy": {
                    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:$PORT",
                    "restartPolicyType": "ON_FAILURE",
                    "restartPolicyMaxRetries": 10
                }
            }
            
            with open('railway.json', 'w') as f:
                json.dump(railway_config, f, indent=2)
            
            # إنشاء Procfile لRailway
            with open('Procfile', 'w') as f:
                f.write('web: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:$PORT\n')
            
            print("✅ ملفات Railway جاهزة")
            print("📋 للنشر على Railway:")
            print("1. اذهب إلى: https://railway.app")
            print("2. اربط GitHub")
            print("3. اختر المشروع")
            print("4. سيتم النشر تلقائياً")
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في إعداد Railway: {e}")
            return False
    
    def deploy_to_render(self):
        """نشر على Render"""
        print("🎨 إعداد النشر على Render...")
        
        try:
            # إنشاء ملف render.yaml
            render_config = """
services:
  - type: web
    name: math-competition-platform
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:$PORT
    envVars:
      - key: DEBUG
        value: False
      - key: DJANGO_SETTINGS_MODULE
        value: alhassan.settings
"""
            
            with open('render.yaml', 'w') as f:
                f.write(render_config)
            
            print("✅ ملفات Render جاهزة")
            print("📋 للنشر على Render:")
            print("1. اذهب إلى: https://render.com")
            print("2. أنشئ Web Service")
            print("3. اربط GitHub")
            print("4. اختر المشروع")
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في إعداد Render: {e}")
            return False
    
    def create_portable_version(self):
        """إنشاء نسخة محمولة"""
        print("💿 إنشاء نسخة محمولة...")
        
        try:
            # إنشاء مجلد النسخة المحمولة
            portable_dir = f"math_platform_portable_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(portable_dir, exist_ok=True)
            
            # نسخ الملفات الأساسية
            files_to_copy = [
                'manage.py',
                'requirements.txt',
                'alhassan/',
                'competitions/',
                'static/',
                'templates/',
                'db.sqlite3'
            ]
            
            for item in files_to_copy:
                if os.path.exists(item):
                    if os.path.isdir(item):
                        shutil.copytree(item, os.path.join(portable_dir, item))
                    else:
                        shutil.copy2(item, portable_dir)
            
            # إنشاء سكريبت تشغيل
            startup_script = """#!/usr/bin/env python3
import subprocess
import sys
import os

def main():
    print("🎯 تشغيل النسخة المحمولة لمنصة المسابقات الرياضية")
    
    try:
        # تثبيت المتطلبات
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        # تطبيق قاعدة البيانات
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        
        # جمع الملفات الثابتة
        subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
        
        # تشغيل الخادم
        print("🚀 تشغيل الخادم على: http://localhost:8000")
        print("👥 رابط التلاميذ: http://localhost:8000/student/login/")
        print("🔑 رمز الدخول: ben25")
        
        subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        input("اضغط Enter للخروج...")

if __name__ == "__main__":
    main()
"""
            
            with open(os.path.join(portable_dir, 'start_portable.py'), 'w', encoding='utf-8') as f:
                f.write(startup_script)
            
            # إنشاء ملف README
            readme_content = """# 💿 النسخة المحمولة لمنصة المسابقات الرياضية

## 🚀 التشغيل:
1. تأكد من تثبيت Python 3.7+
2. شغل: python start_portable.py
3. اذهب إلى: http://localhost:8000/student/login/
4. رمز الدخول: ben25

## 📋 المتطلبات:
- Python 3.7+
- اتصال بالإنترنت (للتثبيت الأولي)

## 🎯 الاستخدام:
- للتلاميذ: http://localhost:8000/student/login/
- للأساتذة: http://localhost:8000/accounts/login/
- رمز الدخول: ben25
"""
            
            with open(os.path.join(portable_dir, 'README.md'), 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f"✅ تم إنشاء النسخة المحمولة في: {portable_dir}")
            return portable_dir
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء النسخة المحمولة: {e}")
            return None
    
    def setup_all_backups(self):
        """إعداد جميع النسخ الاحتياطية"""
        print("🔄 إعداد جميع النسخ الاحتياطية...")
        
        results = {}
        
        # إعداد البدائل
        for name, method in self.backup_methods.items():
            try:
                print(f"\n📋 إعداد {name}...")
                results[name] = method()
            except Exception as e:
                print(f"❌ فشل في إعداد {name}: {e}")
                results[name] = False
        
        # إنشاء النسخة المحمولة
        portable_dir = self.create_portable_version()
        results['portable'] = portable_dir is not None
        
        # حفظ تقرير النسخ الاحتياطية
        backup_report = {
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'active_backups': [backup['name'] for backup in self.active_backups],
            'portable_directory': portable_dir
        }
        
        with open('backup_report.json', 'w', encoding='utf-8') as f:
            json.dump(backup_report, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*50)
        print("📊 تقرير النسخ الاحتياطية:")
        print("="*50)
        
        for name, success in results.items():
            status = "✅ نجح" if success else "❌ فشل"
            print(f"{name}: {status}")
        
        print(f"\n📄 تم حفظ التقرير في: backup_report.json")
        
        return results

def main():
    """الدالة الرئيسية"""
    print("🔄 نظام النسخ الاحتياطية لمنصة المسابقات الرياضية")
    print("="*60)
    
    backup_system = BackupDeployment()
    results = backup_system.setup_all_backups()
    
    print("\n🎯 النسخ الاحتياطية جاهزة!")
    print("📋 يمكنك الآن استخدام أي من البدائل المتاحة")

if __name__ == "__main__":
    main()
