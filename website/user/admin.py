from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    
    list_display = ('email', 'username', 'is_admin', 'is_staff')
    list_filter = ('is_admin', 'is_staff', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('username',)}),
        ('Permisos', {'fields': (
            'is_admin', 
            'is_active', 
            'is_staff',     
            'is_superuser', 
            'groups',       
            'user_permissions' 
        )}),
        ('Fechas importantes', {'fields': ('last_login',)}),
    )
    
    filter_horizontal = ('groups', 'user_permissions')
    
    ordering = ('email',)

admin.site.register(User, UserAdmin)