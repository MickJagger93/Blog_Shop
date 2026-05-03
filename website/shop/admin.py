from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin, ExportMixin
from .models import Category, Product, UserActivity
from .widgets import CloudinaryImageWidget
from django.utils.text import slugify

class ProductResource(resources.ModelResource):
    
    category = fields.Field(
        column_name='category',
        attribute='category',
        
        widget=ForeignKeyWidget(Category, 'name')
    )

    image = fields.Field(
        column_name='image',
        attribute='image',
        widget=CloudinaryImageWidget()
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'price', 'stock', 'is_active', 'image')
        import_id_fields = ('id',)

    def before_import_row(self, row, **kwargs):
        
        if 'slug' not in row or not row['slug']:
            if 'name' in row and row['name']:
                row['slug'] = slugify(row['name'])

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
