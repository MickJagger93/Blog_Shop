from import_export.widgets import Widget

class CloudinaryImageWidget(Widget):
    
    def clean(self, value, row=None, *args, **kwargs):
        
        return str(value).strip() if value else None

    def render(self, value, obj=None):
        
        if not value:
            return ""
        if hasattr(value, 'public_id'):
            return value.public_id
        return str(value)


