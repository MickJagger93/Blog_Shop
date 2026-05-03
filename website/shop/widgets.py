import re
from import_export.widgets import Widget

class CloudinaryImageWidget(Widget):
   
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        
        val_str = str(value).strip()

        if "image/upload/" in val_str:
            val_str = val_str.split("image/upload/")[-1]

        val_str = re.sub(r'^v\d+/', '', val_str)

        public_id = val_str.split(".")[0]

        return public_id

    def render(self, value, obj=None):
        
        if not value:
            return ""
        
        if hasattr(value, 'public_id'):
            return value.public_id
        return str(value)


