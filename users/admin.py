from django.contrib import admin
from users.models import *
# Register your models here.
from .models import CustomUser, Address, UserAttachments ,EmailVerificationCode

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type']
    list_filter = ['user_type']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # إظهار العناوين الخاصة بالمستخدم فقط
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
admin.site.register(EmailVerificationCode)
admin.site.register(UserAttachments)
