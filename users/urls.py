from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users import views
urlpatterns = [
    path('register_user/',views.RegisterView.as_view() ,name='register_user'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('resend/', views.ResendVerificationCodeView.as_view(), name='resend'),
    path('verify_email_code/',views.VerifyOTPView.as_view() ,name='verify_email_code'),
   # path('whatsapp/',views.send_whatsapp_message ,name='whatsapp'),
    
]
urlpatterns = format_suffix_patterns(urlpatterns)
