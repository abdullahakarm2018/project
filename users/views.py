from django.shortcuts import render
from users.serializers import *
from users.email import *
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from rest_framework import status
# Create your views here.


@api_view(['POST'])
def register_api(request):
    if request.method == 'POST':
        data=request.data
        serializer =ProfileSerializer(data=data)
        phone_number_api = data['phone_number']
        try:
            phone = Profile.objects.get(phone_number=phone_number_api)
        except Profile.DoesNotExist:
            phone = None
        print(phone_number_api)
        otp = random.randint(100000,999999)
        if phone == None:
            if serializer.is_valid(raise_exception=True):
                serializer.save(otp=otp)
                context = {'message' : 'Registration Successfully Check Email','data':serializer.data,'status':status.HTTP_201_CREATED}
            return Response(serializer.data,status=status.HTTP_200_OK)
        phone.otp=otp
        return Response("Successfully")
    return Response({'message' : 'Something Went Wrong'},serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    