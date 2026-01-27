from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    # جلب أسماء الحقول المرتبطة بدلاً من الـ ID
    category_name = serializers.ReadOnlyField(source='category.name')
    unit_name = serializers.ReadOnlyField(source='main_unit.name')
    company_name = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'image', 'product_type', 'price', 
            'category', 'category_name', 
            'main_unit', 'unit_name',
            'company', 'company_name',
            'is_global', 'price_type', 'package','barcode'
        ]
        read_only_fields = ['created_user', 'updated_user']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_user', 'updated_user']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ['created_user', 'updated_user']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['created_user', 'updated_user']

class PriceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceType
        fields = '__all__'
        read_only_fields = ['created_user', 'updated_user']


