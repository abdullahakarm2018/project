from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# Create your views here.

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_user == request.user



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # السماح بالوصول للمنتجات العامة دون تسجيل دخول
    def get_permissions(self):
        if self.action == 'public_products':
            return [AllowAny()]
        return [IsAuthenticated()]

    # هذا المسار سيصبح: /product/products/public_products/
    @action(detail=False, methods=['get'], url_path='public_products')
    def public_products(self,request):
        # تصفية المنتجات التي تم تعليمها كـ عالمية وموافقة عليها
        products = Product.objects.filter(is_global=True, is_approved=True)
        serializer = self.get_serializer(products, many=True)
        
        # هنا نرسل الـ is_global في ترويسة الرد كما طلبت
        return Response(
             serializer.data
        )



class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated,IsOwner]
    def perform_create(self, serializer):
        serializer.save(created_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_user=self.request.user)

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated,IsOwner]
    def perform_create(self, serializer):
        serializer.save(created_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated,IsOwner]
    def perform_create(self, serializer):
        serializer.save(created_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_user=self.request.user)