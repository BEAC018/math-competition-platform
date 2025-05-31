#!/usr/bin/env python3
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
        print("\n✅ تم إيقاف المنصة")

if __name__ == "__main__":
    main()
