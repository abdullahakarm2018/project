from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class MultiFieldAuthBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # البحث عبر البريد الإلكتروني أو الجوال أو اسم المستخدم
            user = UserModel.objects.get(
                Q(username=username) | 
                Q(email=username) | 
                Q(phone_number=username)
            )
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None