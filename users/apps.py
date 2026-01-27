# users/apps.py
from django.apps import AppConfig
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # استيراد الإشارات هنا فقط بعد تحميل التطبيقات
        import users.signals  # تأكد من أن هذا الملف لا يحتوي على استيرادات خاطئة