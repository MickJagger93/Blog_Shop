from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

class Order(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuario")
    full_name = models.CharField(max_length=100, verbose_name="Nombre Completo")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    city = models.CharField(max_length=50, verbose_name="Ciudad")
    postal_code = models.CharField(max_length=20, verbose_name="Código postal")
    country = CountryField(blank_label='(Select country)', verbose_name="País")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    paid = models.BooleanField(default=False, verbose_name="¿Pagado?")

    def __str__(self):
        return f'Pedido {self.id} - {self.full_name}'


class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Pedido")
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, verbose_name="Producto")
    stock = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")  

    def __str__(self):
        return f'{self.stock} x {self.product.name}'