from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_otp_email_task(subject, message, email, otp_code):

    send_mail(subject,
              message,
              settings.EMAIL_HOST_USER,
              [email],
              fail_silently=False)
    return f"OTP Email successfully sent to {email}"