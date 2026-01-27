from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets
#from users.views import send_whatsapp_message
# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('SP', 'ServiceProvider'),  # مزود خدمة
        ('SC', 'ServiceConsumer'),  # مستهلك خدمة
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    id_device = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="users", null=True, blank=True)
    user_type = models.CharField(max_length=5, choices=USER_TYPES, default='SC')
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.username
class EmailVerificationCode(models.Model):
    # استخدم settings.AUTH_USER_MODEL لـ ForeignKey لنموذج المستخدم
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    # قم بتمرير دالة (callable) إلى default لرموز فريدة لكل مثيل
    code = models.CharField(max_length=20,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False) # للإشارة إلى استخدام الرمز

    def is_valid(self):
        # قم بتعريف منطق الصلاحية هنا، على سبيل المثال، انتهاء الصلاحية بعد 5 دقائق
        # تأكد من أن 'is_used' جزء من التحقق من الصلاحية
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        return not self.is_used and self.created_at >= five_minutes_ago

    def __str__(self):
        return f"Code for {self.user.username if self.user else 'No User'}: {self.code}"


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True)
    longitude = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)
    address_line_1 = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    postal_code = models.CharField(max_length=20,blank=True,null=True)
    
    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country}"

class UserAttachments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True)
    file_name = models.CharField(max_length=255,blank=True,null=True)
    file_path = models.FileField(upload_to="userattachments",blank=True,null=True)
    file_type = models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def save(self, *args, **kwargs):
        # التحقق من نوع الملف
        if not self.file_path.name.endswith(('.jpg', '.png', '.pdf')):
            raise ValueError("Only JPG, PNG, and PDF files are allowed.")
        super().save(*args, **kwargs)

class Meta:
    permissions = [
        ("can_access_admin_panel", "Can Access Admin Panel"),
        ("can_upload_files", "Can Upload Files"),
    ]

    user_id =models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    file_name = models.CharField(max_length=255,null=True,blank=True)
    file_path = models.ImageField( upload_to="userattachments", null=True,blank=True)
    file_size =  models.CharField(max_length=255,null=True,blank=True)
    file_type = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True,null=True)
    updated_at = models.DateTimeField(auto_now = True, blank = True,null=True)

    def __str__(self):
        return self.file_name 