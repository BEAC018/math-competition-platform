#!/usr/bin/env python3
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
            print("\n✅ تم إيقاف الخادم بواسطة المستخدم")
            break
        except Exception as e:
            print(f"❌ خطأ: {e}")
            print("⏳ إعادة المحاولة خلال 10 ثوان...")
            time.sleep(10)

if __name__ == "__main__":
    keep_server_running()
