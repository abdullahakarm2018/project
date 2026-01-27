import re
from django.core.mail import send_mail
import random
from django.conf import settings
from django.contrib.auth.models import User 
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def is_valid_email(email):
    """تحقق من أن عنوان البريد الإلكتروني صالح."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None
def send_otp_via_email(email, otp):
    if not is_valid_email(email):
        print(f"عنوان البريد الإلكتروني {email} غير صالح.")
        return False
    try:
        subject = "رمز التحقق الخاص بك"
        html_message = render_to_string('emails/otp_email.html', {'otp': otp})
        plain_message = strip_tags(html_message)  # نص عادي للبريد الإلكتروني
        email_from = settings.EMAIL_HOST_USER

        send_mail(subject, plain_message, email_from, [email], html_message=html_message)

        user_obj = User.objects.get(email=email)
        user_obj.otp = otp
        user_obj.save()

        return True

    except User.DoesNotExist:
        print(f"User with email {email} does not exist.")
        return False

    except Exception as e:
        print(f"An error occurred while sending the email:{e}")
        return False