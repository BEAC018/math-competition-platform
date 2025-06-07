#!/usr/bin/env python3
"""
📱 تطبيق المسابقات الرياضية للهاتف النقال - نسخة مبسطة
Mobile Math Competition App - Simplified Version
"""

import os
import sys
import threading
import time
import subprocess
import socket
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.config import Config

# إعداد Kivy للهاتف
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

class SplashScreen(Screen):
    """شاشة البداية"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # شعار التطبيق
        title = Label(
            text='🧮 منصة المسابقات الرياضية',
            font_size='24sp',
            size_hint=(1, 0.3),
            halign='center'
        )
        
        subtitle = Label(
            text='تطبيق الهاتف النقال\nنفس الميزات 100%',
            font_size='16sp',
            size_hint=(1, 0.2),
            halign='center'
        )
        
        # زر البدء
        start_btn = Button(
            text='🚀 بدء التطبيق',
            size_hint=(1, 0.2),
            font_size='18sp'
        )
        start_btn.bind(on_press=self.start_app)
        
        # معلومات التطبيق
        info = Label(
            text='• جميع ميزات النسخة الأصلية\n• مسابقات رياضية تفاعلية\n• إحصائيات وتقارير\n• يعمل بدون إنترنت',
            font_size='14sp',
            size_hint=(1, 0.3),
            halign='center'
        )
        
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(start_btn)
        layout.add_widget(info)
        
        self.add_widget(layout)
    
    def start_app(self, instance):
        """بدء التطبيق الرئيسي"""
        app = App.get_running_app()
        app.start_django_server()
        app.root.current = 'loading'

class LoadingScreen(Screen):
    """شاشة التحميل"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(
            text='⏳ جاري تحميل التطبيق...',
            font_size='20sp',
            size_hint=(1, 0.3),
            halign='center'
        )
        
        self.status_label = Label(
            text='🔄 بدء تشغيل الخادم المحلي...',
            font_size='16sp',
            size_hint=(1, 0.4),
            halign='center'
        )
        
        info = Label(
            text='يرجى الانتظار بضع ثوان\nحتى يتم تحميل جميع الميزات',
            font_size='14sp',
            size_hint=(1, 0.3),
            halign='center'
        )
        
        layout.add_widget(title)
        layout.add_widget(self.status_label)
        layout.add_widget(info)
        
        self.add_widget(layout)
    
    def update_status(self, message):
        """تحديث رسالة الحالة"""
        self.status_label.text = message

class MainScreen(Screen):
    """الشاشة الرئيسية مع أزرار التنقل"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # عنوان التطبيق
        title = Label(
            text='🧮 منصة المسابقات الرياضية',
            font_size='20sp',
            size_hint=(1, 0.15),
            halign='center'
        )
        
        # معلومات الخادم
        self.server_info = Label(
            text='🌐 الخادم: http://127.0.0.1:8000\n✅ يعمل بشكل طبيعي',
            font_size='14sp',
            size_hint=(1, 0.15),
            halign='center'
        )
        
        # أزرار التنقل الرئيسية
        nav_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.6))
        
        home_btn = Button(
            text='🏠 الصفحة الرئيسية',
            font_size='16sp',
            size_hint=(1, 0.2)
        )
        home_btn.bind(on_press=lambda x: self.open_url('http://127.0.0.1:8000/'))
        
        student_btn = Button(
            text='👥 دخول الطلاب',
            font_size='16sp',
            size_hint=(1, 0.2)
        )
        student_btn.bind(on_press=lambda x: self.open_url('http://127.0.0.1:8000/student/login/'))
        
        teacher_btn = Button(
            text='👨‍🏫 دخول المعلمين',
            font_size='16sp',
            size_hint=(1, 0.2)
        )
        teacher_btn.bind(on_press=lambda x: self.open_url('http://127.0.0.1:8000/accounts/login/'))
        
        admin_btn = Button(
            text='⚙️ لوحة الإدارة',
            font_size='16sp',
            size_hint=(1, 0.2)
        )
        admin_btn.bind(on_press=lambda x: self.open_url('http://127.0.0.1:8000/admin/'))
        
        browser_btn = Button(
            text='🌐 فتح في المتصفح',
            font_size='16sp',
            size_hint=(1, 0.2)
        )
        browser_btn.bind(on_press=lambda x: self.open_url('http://127.0.0.1:8000/'))
        
        nav_layout.add_widget(home_btn)
        nav_layout.add_widget(student_btn)
        nav_layout.add_widget(teacher_btn)
        nav_layout.add_widget(admin_btn)
        nav_layout.add_widget(browser_btn)
        
        # معلومات الدخول
        login_info = Label(
            text='🔑 رمز دخول الطلاب: ben25\n👨‍💼 المدير: admin',
            font_size='12sp',
            size_hint=(1, 0.1),
            halign='center'
        )
        
        layout.add_widget(title)
        layout.add_widget(self.server_info)
        layout.add_widget(nav_layout)
        layout.add_widget(login_info)
        
        self.add_widget(layout)
    
    def open_url(self, url):
        """فتح الرابط في المتصفح"""
        try:
            webbrowser.open(url)
        except Exception as e:
            Logger.error(f'Error opening URL: {e}')

class MathCompetitionApp(App):
    """التطبيق الرئيسي"""
    
    def build(self):
        """بناء واجهة التطبيق"""
        self.title = 'منصة المسابقات الرياضية'
        
        # إنشاء مدير الشاشات
        sm = ScreenManager()
        
        # إضافة الشاشات
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(MainScreen(name='main'))
        
        # البدء بشاشة البداية
        sm.current = 'splash'
        
        return sm
    
    def start_django_server(self):
        """تشغيل خادم Django في خيط منفصل"""
        def run_server():
            try:
                # تحديث الحالة
                Clock.schedule_once(lambda dt: self.update_loading_status('📊 تحضير قاعدة البيانات...'), 0)
                
                # تشغيل الهجرات
                subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                             cwd=self.get_django_path(), check=True, 
                             capture_output=True)
                
                Clock.schedule_once(lambda dt: self.update_loading_status('📁 تجميع الملفات الثابتة...'), 1)
                
                # تجميع الملفات الثابتة
                subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                             cwd=self.get_django_path(), check=True, 
                             capture_output=True)
                
                Clock.schedule_once(lambda dt: self.update_loading_status('🚀 تشغيل الخادم...'), 2)
                
                # تشغيل الخادم
                self.django_process = subprocess.Popen([
                    sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'
                ], cwd=self.get_django_path())
                
                # انتظار تشغيل الخادم
                time.sleep(5)
                
                # التحقق من تشغيل الخادم
                if self.check_server():
                    Clock.schedule_once(lambda dt: self.server_ready(), 0)
                else:
                    Clock.schedule_once(lambda dt: self.server_error(), 0)
                    
            except Exception as e:
                Logger.error(f'Django Server Error: {e}')
                Clock.schedule_once(lambda dt: self.server_error(), 0)
        
        # تشغيل في خيط منفصل
        threading.Thread(target=run_server, daemon=True).start()
    
    def get_django_path(self):
        """الحصول على مسار مشروع Django"""
        # البحث عن ملف manage.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.exists(os.path.join(current_dir, 'manage.py')):
            return current_dir
        
        # البحث في المجلد الأب
        parent_dir = os.path.dirname(current_dir)
        if os.path.exists(os.path.join(parent_dir, 'manage.py')):
            return parent_dir
        
        return current_dir
    
    def check_server(self):
        """التحقق من تشغيل الخادم"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 8000))
            sock.close()
            return result == 0
        except:
            return False
    
    def update_loading_status(self, message):
        """تحديث رسالة التحميل"""
        loading_screen = self.root.get_screen('loading')
        loading_screen.update_status(message)
    
    def server_ready(self):
        """الخادم جاهز"""
        self.update_loading_status('✅ التطبيق جاهز!')
        time.sleep(1)
        self.root.current = 'main'
    
    def server_error(self):
        """خطأ في الخادم"""
        self.update_loading_status('❌ خطأ في تشغيل الخادم')
    
    def on_stop(self):
        """إيقاف التطبيق"""
        if hasattr(self, 'django_process'):
            self.django_process.terminate()

if __name__ == '__main__':
    MathCompetitionApp().run()
