from django.core.mail import send_mail
import random
from django.conf import settings
from users.models import Profile
def send_otp_via_email(email):
    subject = "kogflkhj"
    otp = random.randint(100000,999999)
    message =f'fdfh {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    user_obj = Profile.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()