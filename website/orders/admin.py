from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'full_name', 'get_email', 'paid', 'created_at']
    list_filter = ['paid', 'created_at']
    list_editable = ['paid']

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email' 


