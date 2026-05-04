import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Order
from user.tasks import send_order_email_sync  

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Order)
def enviar_notificaciones_orden(sender, instance, created, **kwargs):
    subject = ""
    message = ""
    recipient = ""

    if created:
        subject = f'🚨 Nueva Orden Pendiente #{instance.id}'
        message = f'Hola Admin, nueva orden de {instance.full_name}.'
        recipient = getattr(settings, 'ADMIN_EMAIL', settings.EMAIL_HOST_USER)
    
    elif instance.paid: 
        subject = f'✅ Pago Confirmado - Orden #{instance.id}'
        message = f'¡Hola {instance.full_name}!\n\nHemos verificado tu depósito exitosamente.'
        recipient = instance.user.email if instance.user else None

    if recipient:
        
        try:
            logger.info(f"Intentando enviar correo síncrono a {recipient}...")
            send_order_email_sync(subject, message, recipient)
            logger.info(f"✅ Correo enviado exitosamente a {recipient}")
        
        except Exception as e:
            logger.error(f"❌ Error crítico enviando correo a {recipient}: {str(e)}")




