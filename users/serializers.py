import random
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.email import send_otp_via_email
from django.conf import settings
from django.apps import apps # استيراد apps
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.hashers import make_password
User = get_user_model() 

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone_number', 'bio', 'location', 'birth_date', 'user_type']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # يمكن أن يكون اسم مستخدم أو بريد أو جوال
    password = serializers.CharField(write_only=True)
    id_device = serializers.CharField(required=False)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        id_device = data.get('id_device')

        if not username or not password:
            raise ValidationError({"detail": "اسم المستخدم وكلمة المرور مطلوبان."})

        user = None
        if '@' in username:
            user = User.objects.filter(email=username).first()
        elif username.isdigit():
            user = User.objects.filter(phone_number=username).first()
        else:
            user = User.objects.filter(username=username).first()

        if not user:
            raise ValidationError({"detail": "المستخدم غير موجود."})

        authenticated_user = authenticate(username=user.username, password=password)
        if not authenticated_user:
            raise ValidationError({"detail": "كلمة المرور غير صحيحة."})
        
        # --- هذا هو الجزء المعدل ---
        # الحالة الأولى: id_device موجود في القاعدة وغير مطابق للجهاز الحالي
        # الحالة الثانية: id_device فارغ في القاعدة (لم يتم تسجيله بعد) ولكن يوجد id_device قادم من الطلب
        if (authenticated_user.id_device and authenticated_user.id_device != id_device) or \
           (not authenticated_user.id_device and id_device):
            
            # إرسال رمز تحقق
            code = random.randint(100000, 999999)
            # تأكد من استيراد EmailVerificationCode ومديلك بشكل صحيح
            from .models import EmailVerificationCode # تأكد من المسار الصحيح
            EmailVerificationCode.objects.create(user=authenticated_user, code=code)
            send_otp_via_email(authenticated_user.email, code) # أو send_sms

            # رفع خطأ مميز لتطبيق Flutter ليعرف أنه يجب الانتقال لصفحة التحقق
            raise ValidationError({"non_field_errors": "DEVICE_MISMATCH_OR_NEW_DEVICE", "detail": "يتطلب التحقق من الجهاز. تم إرسال رمز التحقق."})

        # إذا وصل الكود إلى هنا، فهذا يعني أن id_device مطابق، أو أن id_device غير موجود في الطلب
        # ولا يوجد id_device في القاعدة (حالة لن تحدث مع المنطق الجديد أعلاه إذا أرسل id_device)
        # أو أن id_device مطابق ولا حاجة للتحقق.

        data['user'] = authenticated_user
        return data

class OTPVerificationSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField()
    id_device = serializers.CharField(required=False)

    def validate(self, data):
        username = data.get('username')
        code = data.get('code')
        id_device = data.get('id_device')

        CustomUser = get_user_model() # الطريقة الموصى بها للحصول على نموذج المستخدم

        # تحديد ما إذا كان المدخل بريدًا إلكترونيًا أم اسم مستخدم
        if '@' in username:
            user = CustomUser.objects.filter(email=username).first()
        else:
            user = CustomUser.objects.filter(username=username).first()

        if not user:
            raise serializers.ValidationError("المستخدم غير موجود.") # User not found.

        verification = EmailVerificationCode.objects.filter(user=user, code=code).last()
        if not verification or not verification.is_valid():
            raise serializers.ValidationError("رمز غير صالح أو منتهي الصلاحية.") # Invalid or expired code.

        # تحديث id_device لكائن 'user' المحدد الذي عثرت عليه
        if id_device:
            # تحقق مما إذا كان نموذج المستخدم يحتوي بالفعل على حقل 'id_device'
            if hasattr(user, 'id_device'):
                user.id_device = id_device
                user.save() # حفظ التغييرات على كائن المستخدم هذا في قاعدة البيانات
            else:
                # اختياريًا، قم بإثارة تحذير أو تعامل مع الموقف إذا لم يكن حقل id_device موجودًا
                print(f"Warning: CustomUser model does not have an 'id_device' field for user {user.username}")

        # ضع علامة على رمز التحقق كـ "مستخدم" لمنع إعادة الاستخدام
        verification.is_used = True
        verification.save()

        data['user'] = user
        return data
    
    
class ResendVerificationSerializer(serializers.Serializer):
    username = serializers.CharField()  # يمكن أن يكون البريد أو اسم المستخدم

    def validate(self, data):
        username = data.get('username')

        # تحديد إذا كان المدخل بريدًا إلكترونيًا أو اسم مستخدم
        if '@' in username:
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(username=username).first()

        if not user:
            raise ValidationError("المستخدم غير موجود.")

        # إنشاء رمز جديد
        code = secrets.token_urlsafe(15)
        verification, created = EmailVerificationCode.objects.update_or_create(
            user=user,
            defaults={'code': code}
        )

        # إرسال الرمز (يمكنك استخدام وظيفة send_email أو send_sms)
        send_otp_via_email(user.email, code)  # استبدل بـ وظيفة الإرسال الخاصة بك

        data['message'] = "تم إعادة إرسال الرمز بنجاح."
        return data

