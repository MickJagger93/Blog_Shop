from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_token(username=None, user_email=None, link=None, **kwargs):
    
    subject = kwargs.get('subject', 'Confirm your account')
    message = kwargs.get('message', f"Hello {username}, click here: {link}")
    
    email_to = user_email or kwargs.get('recipient_list', [None])[0]

    if email_to:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email_to],
            fail_silently=False,
        )

@shared_task
def send_order_email(subject, message, recipient_email):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [recipient_email],
        fail_silently=False,
    )
