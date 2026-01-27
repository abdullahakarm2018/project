# shops/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import get_object_or_404

from product.models import Category
from product.serializers import CategorySerializer
from product.views import IsOwner

from shops.models import ProductShop, Shop
from shops.serializers import ProductShopCreateSerializer, ProductShopSerializer, ProductShopUpdateSerializer

class ShopProductsAPIView(APIView):
    """
    عرض جميع منتجات المتجر المرتبطة بالمستخدم الحالي مع بيانات المنتج وسعر التكلفة وسعر البيع.
    """
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        try:
            shop = Shop.objects.get(owner=request.user)
        except Shop.DoesNotExist:
            return Response({'error': 'المتجر غير موجود لهذا المستخدم.'}, status=404)

        product_shops = ProductShop.objects.select_related('product').filter(shop=shop)
        serializer = ProductShopSerializer(product_shops, many=True)
        return Response(serializer.data)


class ShopCategoriesAPIView(APIView):
    """
    عرض الفئات التي تحتوي على منتجات داخل المتجر المرتبط بالمستخدم.
    """
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        try:
            shop = Shop.objects.get(owner=request.user)
        except Shop.DoesNotExist:
            return Response({'error': 'المتجر غير موجود لهذا المستخدم.'}, status=404)

        categories = Category.objects.filter(
            product__productshop__shop=shop
        ).distinct()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ProductShopByShopAPIView(generics.ListAPIView):
    """
    عرض منتجات متجر محدد عبر ID.
    """
    serializer_class = ProductShopSerializer
    permission_classes = [IsAuthenticated]  # عدل حسب الحاجة

    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        return ProductShop.objects.select_related('product').filter(shop_id=shop_id)


class ProductShopCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request):
        try:
            shop = Shop.objects.get(owner=request.user)
        except Shop.DoesNotExist:
            return Response({'error': 'المتجر غير موجود لهذا المستخدم.'}, status=404)

        serializer = ProductShopCreateSerializer(
            data=request.data,
            context={'shop': shop, 'user': request.user}
        )

        if serializer.is_valid():
            product_shop = serializer.save()
            output_serializer = ProductShopSerializer(product_shop)
            return Response(output_serializer.data, status=201)

        return Response(serializer.errors, status=400)

class ProductShopUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def patch(self, request, pk):
        try:
            product_shop = ProductShop.objects.select_related('shop').get(pk=pk)
        except ProductShop.DoesNotExist:
            return Response({'error': 'المنتج غير موجود في هذا المتجر.'}, status=404)

        # تحقق من أن المستخدم يملك المتجر
        if product_shop.shop.owner != request.user:
            return Response({'error': 'ليس لديك صلاحية التعديل على هذا المنتج.'}, status=403)

        serializer = ProductShopUpdateSerializer(product_shop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_user=request.user)
            return Response({'message': 'تم التحديث بنجاح.'})
        return Response(serializer.errors, status=400)
    
# shops/views.py

class ProductShopDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, pk):
        try:
            product_shop = ProductShop.objects.select_related('shop').get(pk=pk)
        except ProductShop.DoesNotExist:
            return Response({'error': 'لم يتم العثور على هذا المنتج في المتجر.'}, status=404)

        # تأكد أن المتجر يعود للمستخدم الحالي
        if product_shop.shop.owner != request.user:
            return Response({'error': 'ليس لديك صلاحية لحذف هذا المنتج.'}, status=403)

        product_shop.delete()
        return Response({'message': 'تم حذف المنتج من المتجر بنجاح.'}, status=204)
