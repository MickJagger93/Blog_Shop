import threading
from django.core.mail import send_mail
from django.conf import settings

def send_token_email_sync(username=None, user_email=None, link=None, **kwargs):
    subject = kwargs.get('subject', 'Confirma tu cuenta')
    message = kwargs.get('message', f"Hola {username}, haz click aquí: {link}")
    email_to = user_email or kwargs.get('recipient_list', [None])[0]

    if email_to:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email_to],
            fail_silently=False,
        )

def send_order_email_sync(subject, message, recipient_email):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [recipient_email],
        fail_silently=False,
    )
