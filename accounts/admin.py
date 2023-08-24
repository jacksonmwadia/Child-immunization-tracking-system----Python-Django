from atexit import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Doctor, Parent,MOH
# Register your models here.

class CustomUserAdmin(UserAdmin):
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_doctor','is_parent')


    fieldsets = (
        (None, {
            "fields": (
                
                'username',
                'email',
                'first_name',
                'last_name',
                'password',
                'phone_no',

            ), 
        }),
        ('Status', {
            "fields": (
                'is_active',
            ), 
        }),
        ("Permissions", {
            "fields": (
                'is_superuser',
                'is_admin',
                'is_staff',
                'is_doctor',
                'is_parent',
                'is_ministry',

            ), 
        }),
        ("Special Permissions", {
            "fields": (
                'user_permissions',
            ), 
        }),
    )
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id','user', 'hospital', 'license_no', 'email', 'phone_no')
    search_fields = ('user__username', 'user__email', 'hospital__name', 'license_no', 'email', 'phone_no')
    list_filter = ('hospital__name',)
    ordering = ('user__username',)
admin.site.register(Doctor, DoctorAdmin)

class ParentAdmin(admin.ModelAdmin):
    list_display = ('parent_id','user', 'phone_no')
    search_fields = ('user__username', 'user__email', 'phone_no')
    list_filter = ('user__username',)
    ordering = ('user__username',)

admin.site.register(Parent, ParentAdmin)

admin.site.register(MOH)