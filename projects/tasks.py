from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_invite(subject, message, from_email, recipient_list):
    """
    Отправка email через Celery.
    """
    send_mail(subject, message, from_email, recipient_list)
    return f"Email sent to {', '.join(recipient_list)}"

@shared_task
def debug_task():
    print("Debug task executed successfully!")
    return "Debug task executed successfully!"
