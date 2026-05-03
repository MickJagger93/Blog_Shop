import cloudinary
from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, Widget
from import_export.admin import ImportExportModelAdmin, ExportMixin
from .models import Category, Product, UserActivity
from django.utils.text import slugify
from cloudinary import CloudinaryResource

class ProductResource(resources.ModelResource):
    
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name'))

    class Meta:
        
        model = Product
        fields = ('name', 'category', 'description', 'price', 'stock', 'is_active')
        import_id_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    resource_class = ProductResource
    list_display = ('name', 'category', 'is_active')

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    
    resource_class = ProductResource 
    list_display = ('name', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class UserActivityResource(resources.ModelResource):
    
    class Meta:
        model = UserActivity
        fields = ('created_at', 'user__username', 'event_type', 'description', 'ip_address')
        export_order = ('created_at', 'user__username', 'event_type', 'description', 'ip_address')

@admin.register(UserActivity)
class UserActivityAdmin(ExportMixin, admin.ModelAdmin):
    
    resource_class = UserActivityResource
    list_display = ('created_at', 'user', 'event_type', 'description', 'ip_address')
    list_filter = ('event_type', 'created_at')
    search_fields = ('description', 'user__username')
    readonly_fields = ('created_at',) 

    def get_event_display(self, obj):
        return obj.get_event_type_display()
    get_event_display.short_description = 'Tipo de Evento'