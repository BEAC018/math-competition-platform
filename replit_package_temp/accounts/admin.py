from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'الملف الشخصي'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_user_type', 'get_grade', 'is_staff')
    list_select_related = ('profile', )
    
    def get_user_type(self, instance):
        return instance.profile.get_user_type_display()
    get_user_type.short_description = 'نوع المستخدم'
    
    def get_grade(self, instance):
        if instance.profile.grade:
            return instance.profile.get_grade_display()
        return '-'
    get_grade.short_description = 'الصف'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# Unregister the default UserAdmin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
