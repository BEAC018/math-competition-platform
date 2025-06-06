from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import connection
import os


class Command(BaseCommand):
    help = 'إعداد قاعدة البيانات تلقائياً'

    def handle(self, *args, **options):
        self.stdout.write('🚀 بدء إعداد قاعدة البيانات...')
        
        try:
            # تشغيل migrations
            self.stdout.write('📊 تشغيل migrations...')
            call_command('makemigrations', verbosity=0)
            call_command('migrate', verbosity=0)
            
            # إنشاء مدير إذا لم يكن موجود
            if not User.objects.filter(is_superuser=True).exists():
                self.stdout.write('👤 إنشاء مدير النظام...')
                User.objects.create_superuser(
                    username='admin',
                    email='admin@mathcompetition.com',
                    password='admin123456',
                    first_name='مدير',
                    last_name='النظام'
                )
                self.stdout.write('✅ تم إنشاء المدير بنجاح')
            
            self.stdout.write('🎉 تم إعداد قاعدة البيانات بنجاح!')
            
        except Exception as e:
            self.stdout.write(f'❌ خطأ في إعداد قاعدة البيانات: {str(e)}')
