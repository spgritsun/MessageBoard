from celery import shared_task
from django.core.mail import send_mail, mail_admins
from django.conf import settings


@shared_task
def send_email_to_admins(subject='Test', message='TestTestTest'):
    mail_admins(subject, message, fail_silently=False)
