#!/usr/bin/env python3
"""
منصة المسابقات الرياضية - ملف التشغيل الرئيسي
Math Competition Platform - Main Launcher
"""

import os
import sys
import time
import threading
import webbrowser
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import socket

# إضافة مسار Django للنظام
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# إعداد متغيرات البيئة
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')

class MathCompetitionLauncher:
    def __init__(self):
        self.server_process = None
        self.server_running = False
        self.port = 8000
        
        # إنشاء النافذة الرئيسية
        self.root = tk.Tk()
        self.root.title("منصة المسابقات الرياضية - Math Competition Platform")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # تعيين أيقونة إذا كانت متوفرة
        try:
            self.root.iconbitmap(BASE_DIR / 'static' / 'favicon.ico')
        except:
            pass
        
        self.setup_ui()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        
        # إطار العنوان
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=20)
        
        title_label = ttk.Label(
            title_frame, 
            text="🧮 منصة المسابقات الرياضية 🧮",
            font=("Arial", 18, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Math Competition Platform",
            font=("Arial", 12)
        )
        subtitle_label.pack()
        
        # إطار الحالة
        status_frame = ttk.LabelFrame(self.root, text="حالة الخادم - Server Status")
        status_frame.pack(pady=20, padx=20, fill="x")
        
        self.status_label = ttk.Label(
            status_frame,
            text="⭕ الخادم متوقف - Server Stopped",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=10)
        
        # إطار الأزرار
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=20)
        
        # زر بدء الخادم
        self.start_button = ttk.Button(
            buttons_frame,
            text="🚀 بدء الخادم - Start Server",
            command=self.start_server,
            width=25
        )
        self.start_button.pack(pady=5)
        
        # زر إيقاف الخادم
        self.stop_button = ttk.Button(
            buttons_frame,
            text="🛑 إيقاف الخادم - Stop Server",
            command=self.stop_server,
            state="disabled",
            width=25
        )
        self.stop_button.pack(pady=5)
        
        # زر فتح المتصفح
        self.browser_button = ttk.Button(
            buttons_frame,
            text="🌐 فتح في المتصفح - Open in Browser",
            command=self.open_browser,
            state="disabled",
            width=25
        )
        self.browser_button.pack(pady=5)
        
        # إطار الروابط
        links_frame = ttk.LabelFrame(self.root, text="الروابط السريعة - Quick Links")
        links_frame.pack(pady=20, padx=20, fill="x")
        
        # رابط الطلاب
        student_frame = ttk.Frame(links_frame)
        student_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(student_frame, text="🎮 دخول الطلاب:").pack(side="left")
        self.student_link = ttk.Label(
            student_frame,
            text="http://localhost:8000/student/login/",
            foreground="blue",
            cursor="hand2"
        )
        self.student_link.pack(side="left", padx=10)
        self.student_link.bind("<Button-1>", lambda e: self.open_url("http://localhost:8000/student/login/"))
        
        # رمز الدخول
        code_frame = ttk.Frame(links_frame)
        code_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(code_frame, text="🔑 رمز الدخول:").pack(side="left")
        ttk.Label(code_frame, text="ben25", font=("Arial", 12, "bold"), foreground="green").pack(side="left", padx=10)
        
        # رابط المعلمين
        teacher_frame = ttk.Frame(links_frame)
        teacher_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(teacher_frame, text="👨‍🏫 دخول المعلمين:").pack(side="left")
        self.teacher_link = ttk.Label(
            teacher_frame,
            text="http://localhost:8000/accounts/login/",
            foreground="blue",
            cursor="hand2"
        )
        self.teacher_link.pack(side="left", padx=10)
        self.teacher_link.bind("<Button-1>", lambda e: self.open_url("http://localhost:8000/accounts/login/"))
        
        # إطار المعلومات
        info_frame = ttk.LabelFrame(self.root, text="معلومات - Information")
        info_frame.pack(pady=20, padx=20, fill="x")
        
        info_text = """
📝 تعليمات الاستخدام:
1. اضغط 'بدء الخادم' لتشغيل المنصة
2. انتظر حتى يصبح الخادم جاهزاً
3. اضغط 'فتح في المتصفح' أو انقر على الروابط
4. للطلاب: استخدم رمز 'ben25' للدخول
5. اضغط 'إيقاف الخادم' عند الانتهاء
        """
        
        ttk.Label(info_frame, text=info_text, justify="right").pack(pady=10)
        
        # زر الخروج
        exit_button = ttk.Button(
            self.root,
            text="❌ خروج - Exit",
            command=self.exit_application,
            width=25
        )
        exit_button.pack(pady=20)
        
    def is_port_available(self, port):
        """التحقق من توفر المنفذ"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return True
        except:
            return False
    
    def start_server(self):
        """بدء خادم Django"""
        try:
            # التحقق من توفر المنفذ
            if not self.is_port_available(self.port):
                messagebox.showerror("خطأ", f"المنفذ {self.port} مستخدم بالفعل!")
                return
            
            # تطبيق الهجرات
            self.status_label.config(text="⏳ تطبيق الهجرات... - Applying migrations...")
            self.root.update()
            
            migrate_cmd = [sys.executable, "manage.py", "migrate"]
            subprocess.run(migrate_cmd, cwd=BASE_DIR, check=True, capture_output=True)
            
            # جمع الملفات الثابتة
            self.status_label.config(text="⏳ جمع الملفات الثابتة... - Collecting static files...")
            self.root.update()
            
            collectstatic_cmd = [sys.executable, "manage.py", "collectstatic", "--noinput"]
            subprocess.run(collectstatic_cmd, cwd=BASE_DIR, check=True, capture_output=True)
            
            # بدء الخادم
            self.status_label.config(text="⏳ بدء الخادم... - Starting server...")
            self.root.update()
            
            server_cmd = [sys.executable, "manage.py", "runserver", f"127.0.0.1:{self.port}"]
            self.server_process = subprocess.Popen(
                server_cmd,
                cwd=BASE_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            # انتظار بدء الخادم
            threading.Thread(target=self.wait_for_server, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في بدء الخادم: {str(e)}")
            self.status_label.config(text="❌ فشل في البدء - Failed to start")
    
    def wait_for_server(self):
        """انتظار بدء الخادم"""
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex(('127.0.0.1', self.port))
                    if result == 0:
                        self.server_running = True
                        self.root.after(0, self.server_started)
                        return
            except:
                pass
            time.sleep(1)
        
        self.root.after(0, lambda: messagebox.showerror("خطأ", "انتهت مهلة انتظار بدء الخادم"))
    
    def server_started(self):
        """تحديث الواجهة عند بدء الخادم"""
        self.status_label.config(text="✅ الخادم يعمل - Server Running")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.browser_button.config(state="normal")
        
        # فتح المتصفح تلقائياً
        threading.Thread(target=lambda: self.open_url("http://localhost:8000/student/login/"), daemon=True).start()
    
    def stop_server(self):
        """إيقاف الخادم"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
            self.server_running = False
            
            self.status_label.config(text="⭕ الخادم متوقف - Server Stopped")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.browser_button.config(state="disabled")
    
    def open_browser(self):
        """فتح المتصفح"""
        self.open_url("http://localhost:8000/student/login/")
    
    def open_url(self, url):
        """فتح رابط في المتصفح"""
        if self.server_running:
            webbrowser.open(url)
        else:
            messagebox.showwarning("تحذير", "يجب بدء الخادم أولاً!")
    
    def exit_application(self):
        """الخروج من التطبيق"""
        if self.server_running:
            if messagebox.askyesno("تأكيد", "الخادم يعمل. هل تريد إيقافه والخروج؟"):
                self.stop_server()
                self.root.quit()
        else:
            self.root.quit()
    
    def run(self):
        """تشغيل التطبيق"""
        self.root.protocol("WM_DELETE_WINDOW", self.exit_application)
        self.root.mainloop()

if __name__ == "__main__":
    # إعداد Django
    import django
    django.setup()
    
    # تشغيل التطبيق
    app = MathCompetitionLauncher()
    app.run()
