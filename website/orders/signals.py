import threading 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Order
from user.tasks import send_order_email_sync  

@receiver(post_save, sender=Order)
def enviar_notificaciones_orden(sender, instance, created, **kwargs):
    subject = ""
    message = ""
    recipient = ""

    if created:
        subject = f'🚨 Nueva Orden Pendiente #{instance.id}'
        message = f'Hola Admin, nueva orden de {instance.full_name}.'
        recipient = settings.ADMIN_EMAIL
    
    elif instance.paid: 
        subject = f'✅ Pago Confirmado - Orden #{instance.id}'
        message = f'¡Hola {instance.full_name}!\n\nHemos verificado tu depósito exitosamente.'
        recipient = instance.user.email

    if recipient:
        thread = threading.Thread(
            target=send_order_email_sync, 
            args=(subject, message, recipient)
        )
        thread.start()



