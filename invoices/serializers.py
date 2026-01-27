from rest_framework import serializers
from .models import StatusInvoice, Invoice, InvoiceItem

class StatusInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusInvoice
        fields = '__all__'

class InvoiceItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    line_total = serializers.ReadOnlyField()
    
    class Meta:
        model = InvoiceItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'note', 'line_total']

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, required=False)
    owner_user_name = serializers.CharField(source='owner_user.get_full_name', read_only=True)
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'owner_user', 'owner_user_name', 'counterparty_user', 
            'shop', 'shop_name', 'status', 'status_name', 'comments', 
            'total', 'note', 'created_at', 'updated_at', 'created_user', 
            'updated_user', 'items'
        ]
        read_only_fields = ['created_at', 'updated_at', 'total']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        invoice = Invoice.objects.create(**validated_data)
        
        # إنشاء عناصر الفاتورة
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        
        # حساب المجموع
        invoice.calculate_total()
        return invoice
    
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        
        # تحديث بيانات الفاتورة
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # تحديث العناصر إذا تم إرسالها
        if items_data is not None:
            # حذف العناصر الحالية
            instance.items.all().delete()
            # إضافة العناصر الجديدة
            for item_data in items_data:
                InvoiceItem.objects.create(invoice=instance, **item_data)
            
            # إعادة حساب المجموع
            instance.calculate_total()
        
        return instance