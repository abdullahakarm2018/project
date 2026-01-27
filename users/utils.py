# utils.py (أنشئ هذا الملف أو ضعه ضمن ملف views.py مؤقتًا)
from django.core.mail import send_mail

from project import settings

def send_verification_email(email, code):
    subject = 'Your verification code'
    message = f'Your verification code is: {code}'
    from_email = settings.EMAIL_HOST_USER  # غيره بما يناسب إعداداتك
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
