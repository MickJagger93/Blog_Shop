from django.db import models
from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

class Post(models.Model):
    
    title = models.CharField(max_length=200, verbose_name="Título")
    content = models.TextField()
    image = CloudinaryField('image', folder='posts_images/', blank=True, null=True, verbose_name="Imagen")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Author")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Vistas")

    def __str__(self):
        return self.title
