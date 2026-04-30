from django.db import models
from django.utils.text import slugify
from user.models import User

from django.db import models

class Category(models.Model):
    
    name = models.CharField(max_length=100, verbose_name="Nombre")
    slug = models.SlugField(unique=True)

    class Meta:

        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name

class Product(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Categoría")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    image = models.ImageField(upload_to='products/%Y/%m/%d', verbose_name="Imagen")
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name="¿Disponible?")

    class Meta:

        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class UserActivity(models.Model):
    
    EVENT_TYPES = (
        ('search', 'Búsqueda'),
        ('view', 'Vista de Producto'),
        ('cart_add', 'Añadido al Carrito'),
        ('cart_remove', 'Eliminado de Carrito'),
        ('purchase', 'Compra Realizada'),
        ('post_view', 'Post Leído'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuario")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, verbose_name="Tipo de evento")
    description = models.TextField(verbose_name="Descripción") 
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Dirección IP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha/Hora")

    class Meta:
        verbose_name = "Actividad de Usuario"
        verbose_name_plural = "Actividades de Usuarios"
        ordering = ['-created_at']

    def __str__(self):
        user_str = self.user.username if self.user else "Anónimo"
        return f"{user_str} - {self.get_event_type_display()} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"