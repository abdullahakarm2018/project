from django.shortcuts import render
from users.serializers import *
from users.email import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from users.utils import send_verification_email
from rest_framework.authtoken.models import Token
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .models import EmailVerificationCode
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.



@login_required
def dashboard(request):
    if request.user.user_type == 'SP':
        # عرض بيانات مزود الخدمة
        return render(request, 'service_provider_dashboard.html')
    else:
        # عرض بيانات المستهلك
        return render(request, 'service_consumer_dashboard.html')
    
from django.contrib.auth.decorators import permission_required

@permission_required('app_name.can_access_admin_panel', login_url='/no-access/')
def admin_panel(request):
    # كود لوحة التحكم
    pass

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return Response({'message': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if get_user_model().objects.filter(username=username).exists():
            return Response({'message': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if get_user_model().objects.filter(email=email).exists():
            return Response({'message': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_user_model().objects.create_user(username=username, email=email, password=password)
        
        code = f"{secrets.randint(100000, 999999)}"
        EmailVerificationCode.objects.create(user=user, code=code)
        send_otp_via_email(email, code)

        return Response({
            'message': 'User registered successfully. Verification code sent.',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'token' :{'access': str(refresh.access_token),
                'refresh': str(refresh),},
                
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'id_device': user.id_device
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # يمكنك إضافة منطق لتسجيل دخول المستخدم هنا إذا لم يكن مسجلاً بالفعل
            # على سبيل المثال، باستخدام دالة login المدمجة في Django:
            # login(request, user)

            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                # قم بتضمين بيانات المستخدم الأخرى التي تريد إرسالها، على سبيل المثال:
                'username': user.username,
                'email': user.email,
                # 'phone_number': user.phone_number, # أزل التعليق إذا كان لديك هذا الحقل
                'id_device': user.id_device if hasattr(user, 'id_device') else None, # إرسال معرف الجهاز المحدث بأمان
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeView(APIView):
    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# دالة بسيطة للتحقق من صحة صيغة الإيميل
def is_valid_email(email):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email)

@api_view(['POST'])
def verification_with_email(request):
    if request.method != 'POST':
        return Response({'message': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    email_or_username = data.get('email')

    if not email_or_username:
        return Response({"message": "Email or Username is required."}, status=status.HTTP_400_BAD_REQUEST)

    user = None

    if is_valid_email(email_or_username):
        # التحقق باستخدام الإيميل
        try:
            user = User.objects.get(email=email_or_username)
        except User.DoesNotExist:
            pass
    else:
        # التحقق باستخدام اسم المستخدم
        try:
            user = User.objects.get(username=email_or_username)
        except User.DoesNotExist:
            pass

    if user:
        return Response({"message": "Verification successful."}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "No user found with the provided email or username."}, status=status.HTTP_404_NOT_FOUND)




def is_valid_email(email):
    """دالة مساعدة للتحقق من صحة البريد الإلكتروني"""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email_code(request):
    identifier = request.data.get('username')  # يمكن أن يكون username أو email
    code = request.data.get('code')
    id_device = request.data.get('id_device')

    if not identifier or not code:
        return Response({'message': 'Identifier and code are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', identifier):
            user = get_user_model().objects.get(email=identifier)
        else:
            user = get_user_model().objects.get(username=identifier)

        verification = EmailVerificationCode.objects.filter(user=user, code=code).last()
        
        if verification and verification.is_valid():
            profile, created = CustomUser.objects.get_or_create(user_id=user)
            profile.id_device = id_device
            profile.save()
            return Response({'message': 'Email verified successfully.'})
        else:
            return Response({'message': 'Invalid or expired code.'}, status=status.HTTP_400_BAD_REQUEST)

    except get_user_model().DoesNotExist:
        return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)