import cloudinary
from import_export.widgets import Widget

class CloudinaryPublicIdWidget(Widget):
    
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        
        public_id = str(value).strip()

        if "image/upload/" in public_id:
           
            public_id = public_id.split("image/upload/")[-1]
            
            if "/" in public_id and public_id.split("/")[0].startswith("v"):
                public_id = "/".join(public_id.split("/")[1:])
            
            public_id = public_id.split(".")[0]

        return cloudinary.CloudinaryResource(public_id=public_id)

