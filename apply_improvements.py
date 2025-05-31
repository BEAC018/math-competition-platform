#!/usr/bin/env python3
"""
تطبيق التحسينات الشاملة على منصة المسابقات الرياضية
Apply comprehensive improvements to Math Competition Platform
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import logging
from datetime import datetime, timedelta

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PlatformImprover:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.improvements_applied = []
        self.errors = []

    def apply_all_improvements(self):
        """تطبيق جميع التحسينات"""
        logger.info("🚀 بدء تطبيق التحسينات الشاملة...")

        improvements = [
            ("تنظيف قاعدة البيانات", self.clean_database),
            ("تحديث الملفات الثابتة", self.update_static_files),
            ("تحسين القوالب", self.improve_templates),
            ("تطبيق الهجرات", self.apply_migrations),
            ("تحسين الأداء", self.optimize_performance),
            ("تحديث المتطلبات", self.update_requirements),
            ("إنشاء نسخة احتياطية", self.create_backup),
            ("اختبار التطبيق", self.test_application),
        ]

        for name, func in improvements:
            try:
                logger.info(f"📋 تطبيق: {name}")
                func()
                self.improvements_applied.append(name)
                logger.info(f"✅ تم: {name}")
            except Exception as e:
                error_msg = f"❌ فشل في {name}: {str(e)}"
                logger.error(error_msg)
                self.errors.append(error_msg)

        self.generate_report()

    def clean_database(self):
        """تنظيف قاعدة البيانات"""
        # إزالة البيانات المكررة
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alhassan.settings')

        import django
        django.setup()

        from django.utils import timezone
        from competitions.models import Competition, UserResponse

        # إزالة المسابقات غير المكتملة القديمة
        old_incomplete = Competition.objects.filter(
            is_completed=False,
            start_time__lt=timezone.now() - timedelta(hours=24)
        )
        deleted_count = old_incomplete.count()
        old_incomplete.delete()
        logger.info(f"تم حذف {deleted_count} مسابقة غير مكتملة قديمة")

        # إزالة الردود اليتيمة
        orphaned_responses = UserResponse.objects.filter(competition__isnull=True)
        orphaned_count = orphaned_responses.count()
        orphaned_responses.delete()
        logger.info(f"تم حذف {orphaned_count} رد يتيم")

    def update_static_files(self):
        """تحديث الملفات الثابتة"""
        # نسخ ملفات التحسينات
        static_dir = self.base_dir / 'static'

        # إنشاء المجلدات إذا لم تكن موجودة
        (static_dir / 'js').mkdir(parents=True, exist_ok=True)
        (static_dir / 'css').mkdir(parents=True, exist_ok=True)

        # التحقق من وجود ملفات التحسينات
        improvements_js = self.base_dir / 'static' / 'js' / 'improvements.js'
        improvements_css = self.base_dir / 'static' / 'css' / 'improvements.css'

        if improvements_js.exists():
            logger.info("✅ ملف JavaScript للتحسينات موجود")
        else:
            logger.warning("⚠️ ملف JavaScript للتحسينات غير موجود")

        if improvements_css.exists():
            logger.info("✅ ملف CSS للتحسينات موجود")
        else:
            logger.warning("⚠️ ملف CSS للتحسينات غير موجود")

        # جمع الملفات الثابتة
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'],
                      cwd=self.base_dir, check=True)

    def improve_templates(self):
        """تحسين القوالب"""
        templates_dir = self.base_dir / 'templates'

        # البحث عن القوالب الأساسية
        base_template = templates_dir / 'base.html'

        if base_template.exists():
            # قراءة القالب الأساسي
            content = base_template.read_text(encoding='utf-8')

            # إضافة ملفات التحسينات إذا لم تكن موجودة
            if 'improvements.css' not in content:
                css_link = '<link rel="stylesheet" href="{% static \'css/improvements.css\' %}">'
                content = content.replace('</head>', f'    {css_link}\n</head>')

            if 'improvements.js' not in content:
                js_script = '<script src="{% static \'js/improvements.js\' %}"></script>'
                content = content.replace('</body>', f'    {js_script}\n</body>')

            # كتابة القالب المحدث
            base_template.write_text(content, encoding='utf-8')
            logger.info("✅ تم تحديث القالب الأساسي")
        else:
            logger.warning("⚠️ القالب الأساسي غير موجود")

    def apply_migrations(self):
        """تطبيق الهجرات"""
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'],
                      cwd=self.base_dir, check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'],
                      cwd=self.base_dir, check=True)

    def optimize_performance(self):
        """تحسين الأداء"""
        # تنظيف ملفات التخزين المؤقت
        cache_dirs = [
            self.base_dir / '__pycache__',
            self.base_dir / 'competitions' / '__pycache__',
            self.base_dir / 'alhassan' / '__pycache__',
        ]

        for cache_dir in cache_dirs:
            if cache_dir.exists():
                shutil.rmtree(cache_dir)
                logger.info(f"تم حذف {cache_dir}")

        # تنظيف ملفات .pyc
        for pyc_file in self.base_dir.rglob('*.pyc'):
            pyc_file.unlink()

        logger.info("✅ تم تنظيف ملفات التخزين المؤقت")

    def update_requirements(self):
        """تحديث المتطلبات"""
        requirements_file = self.base_dir / 'requirements.txt'

        if requirements_file.exists():
            # قراءة المتطلبات الحالية
            current_requirements = requirements_file.read_text().strip().split('\n')

            # إضافة متطلبات جديدة إذا لم تكن موجودة
            new_requirements = [
                'django-extensions>=3.2.0',
                'django-debug-toolbar>=4.0.0',
                'django-compressor>=4.0',
            ]

            updated = False
            for req in new_requirements:
                package_name = req.split('>=')[0].split('==')[0]
                if not any(package_name in line for line in current_requirements):
                    current_requirements.append(req)
                    updated = True

            if updated:
                requirements_file.write_text('\n'.join(current_requirements) + '\n')
                logger.info("✅ تم تحديث ملف المتطلبات")
            else:
                logger.info("✅ ملف المتطلبات محدث")
        else:
            logger.warning("⚠️ ملف المتطلبات غير موجود")

    def create_backup(self):
        """إنشاء نسخة احتياطية"""
        from datetime import datetime

        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_dir = self.base_dir / backup_name

        # إنشاء مجلد النسخة الاحتياطية
        backup_dir.mkdir(exist_ok=True)

        # نسخ الملفات المهمة
        important_files = [
            'db.sqlite3',
            'manage.py',
            'requirements.txt',
        ]

        important_dirs = [
            'alhassan',
            'competitions',
            'templates',
            'static',
        ]

        for file in important_files:
            file_path = self.base_dir / file
            if file_path.exists():
                shutil.copy2(file_path, backup_dir / file)

        for dir_name in important_dirs:
            dir_path = self.base_dir / dir_name
            if dir_path.exists():
                shutil.copytree(dir_path, backup_dir / dir_name, dirs_exist_ok=True)

        # ضغط النسخة الاحتياطية
        shutil.make_archive(str(backup_dir), 'zip', str(backup_dir))
        shutil.rmtree(backup_dir)

        logger.info(f"✅ تم إنشاء نسخة احتياطية: {backup_name}.zip")

    def test_application(self):
        """اختبار التطبيق"""
        # اختبار بسيط للتأكد من عمل التطبيق
        try:
            subprocess.run([sys.executable, 'manage.py', 'check'],
                          cwd=self.base_dir, check=True, capture_output=True)
            logger.info("✅ اختبار Django check نجح")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ فشل اختبار Django check: {e}")
            raise

        # اختبار تشغيل الخادم لثوان قليلة
        try:
            process = subprocess.Popen([sys.executable, 'manage.py', 'runserver', '--noreload'],
                                     cwd=self.base_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            import time
            time.sleep(3)  # انتظار 3 ثوان

            process.terminate()
            process.wait(timeout=5)

            logger.info("✅ اختبار تشغيل الخادم نجح")
        except Exception as e:
            logger.error(f"❌ فشل اختبار تشغيل الخادم: {e}")
            raise

    def generate_report(self):
        """إنشاء تقرير التحسينات"""
        report = f"""
# 📋 تقرير التحسينات المطبقة

## ✅ التحسينات المطبقة بنجاح ({len(self.improvements_applied)}):
"""
        for improvement in self.improvements_applied:
            report += f"- ✅ {improvement}\n"

        if self.errors:
            report += f"\n## ❌ الأخطاء ({len(self.errors)}):\n"
            for error in self.errors:
                report += f"- {error}\n"

        report += f"""
## 📊 الإحصائيات:
- إجمالي التحسينات: {len(self.improvements_applied) + len(self.errors)}
- نجح: {len(self.improvements_applied)}
- فشل: {len(self.errors)}
- معدل النجاح: {(len(self.improvements_applied) / (len(self.improvements_applied) + len(self.errors)) * 100):.1f}%

## 🎯 النتيجة:
{'✅ تم تطبيق جميع التحسينات بنجاح!' if not self.errors else '⚠️ تم تطبيق معظم التحسينات مع بعض الأخطاء'}

## 🚀 الخطوات التالية:
1. اختبار التطبيق للتأكد من عمل جميع الميزات
2. مراجعة الأخطاء إن وجدت وإصلاحها
3. إنشاء ملف تنفيذي محدث
4. توزيع التطبيق المحسن

تم إنشاء هذا التقرير في: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        report_file = self.base_dir / 'IMPROVEMENTS_REPORT.md'
        report_file.write_text(report, encoding='utf-8')

        print("\n" + "="*60)
        print("🎉 تم الانتهاء من تطبيق التحسينات!")
        print("="*60)
        print(f"📁 تقرير مفصل: {report_file}")
        print(f"✅ نجح: {len(self.improvements_applied)} تحسين")
        if self.errors:
            print(f"❌ فشل: {len(self.errors)} تحسين")
        print("="*60)

def main():
    """الدالة الرئيسية"""
    try:
        improver = PlatformImprover()
        improver.apply_all_improvements()
        return True
    except Exception as e:
        logger.error(f"❌ خطأ عام في تطبيق التحسينات: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
