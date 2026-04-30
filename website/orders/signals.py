from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Order
from user.tasks import send_order_email 

@receiver(post_save, sender=Order)
def enviar_notificaciones_orden(sender, instance, created, **kwargs):
    
    if created:
        subject = f'🚨 Nueva Orden Pendiente #{instance.id}'
        message = f'Hola Admin, nueva orden de {instance.full_name}.'
        send_order_email.delay(subject, message, settings.ADMIN_EMAIL)
    
    else:
        
        if instance.paid:
            subject = f'✅ Pago Confirmado - Orden #{instance.id}'
            message = f'¡Hola {instance.full_name}!\n\nHemos verificado tu depósito exitosamente.'
            send_order_email.delay(subject, message, instance.user.email)



