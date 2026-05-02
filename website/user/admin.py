from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    
    list_display = ('email', 'username', 'is_admin')
    list_filter = ('is_admin',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('username',)}),
        ('Permisos', {'fields': ('is_admin', 'is_active')}),
    )
    
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)