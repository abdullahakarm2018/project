# payments/serializers.py
from rest_framework import serializers

from payments.models import InvoicePayment
from product.models import Product
from product.serializers import ProductSerializer
from .models import  ProductShop

class InvoicePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoicePayment
        fields = '__all__'

class ProductShopSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductShop
        fields = '__all__'

class ProductShopCreateSerializer(serializers.ModelSerializer):
    # أضفنا allow_null لضمان عدم حدوث خطأ إذا أرسل الفرونت إند قيمة null
    product_id = serializers.IntegerField(required=False, allow_null=True)
    product_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = ProductShop
        fields = ['product_id', 'product_name', 'costPrice', 'sellingPrice', 'lessAmount', 'note']

    def validate(self, attrs):
        p_id = attrs.get('product_id')
        p_name = attrs.get('product_name')

        # التحقق من أن أحدهما على الأقل موجود وغير فارغ
        if not p_id and not p_name:
            raise serializers.ValidationError("يجب اختيار منتج موجود أو إدخال اسم منتج جديد.")
        return attrs

    def create(self, validated_data):
        shop = self.context['shop']
        user = self.context['user']
        
        product_id = validated_data.get('product_id')
        product_name = validated_data.get('product_name')

        # 🟢 الحالة 1: إذا تم إرسال معرف المنتج (ربط بمنتج عام موجود)
        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                # التأكد من أن المنتج ليس خاصاً بمتجر آخر
                if product.created_by_shop and product.created_by_shop != shop:
                    raise serializers.ValidationError("لا يمكنك استخدام منتج خاص بمتجر آخر.")
            except Product.DoesNotExist:
                raise serializers.ValidationError("المنتج المختار غير موجود.")

        # 🟢 الحالة 2: إذا كان المعرف فارغاً والاسم موجود (إنشاء منتج خاص جديد)
        elif product_name:
            product = Product.objects.create(
                name=product_name,
                is_global=False,      # غير عالمي
                is_approved=False,    # غير معتمد (يحتاج مراجعة الإدارة)
                created_by_shop=shop, # مرتبط بمتجرك فقط
                created_user=user,
                updated_user=user,
                lessAmount=validated_data.get('lessAmount', 0),
                price=validated_data.get('sellingPrice', 0),
                note=validated_data.get('note', ''),
            )
        
        # 🔒 منع تكرار نفس المنتج في نفس المتجر
        if ProductShop.objects.filter(shop=shop, product=product).exists():
            raise serializers.ValidationError("هذا المنتج مضاف بالفعل في قائمة متجرك.")

        # 🔵 إنشاء الربط النهائي في جدول ProductShop
        return ProductShop.objects.create(
            shop=shop,
            product=product,
            costPrice=validated_data.get('costPrice', 0),
            sellingPrice=validated_data.get('sellingPrice', 0),
            lessAmount=validated_data.get('lessAmount', 0),
            note=validated_data.get('note', ''),
            created_user=user,
            updated_user=user
        )
class ProductShopUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductShop
        fields = [
            'costPrice', 'sellingPrice', 'lessAmount', 'note'
        ]

