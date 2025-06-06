# Migration to create default admin user

from django.db import migrations
from django.contrib.auth.models import User


def create_admin_user(apps, schema_editor):
    """إنشاء مستخدم مدير افتراضي"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@mathcompetition.com',
            password='admin123456',
            first_name='مدير',
            last_name='النظام'
        )


def delete_admin_user(apps, schema_editor):
    """حذف المستخدم المدير"""
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin_user, delete_admin_user),
    ]
