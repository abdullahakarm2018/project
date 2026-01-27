from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from shops.models import Shop
from .models import StatusInvoice, Invoice, InvoiceItem
from .serializers import StatusInvoiceSerializer, InvoiceSerializer, InvoiceItemSerializer

class StatusInvoiceViewSet(viewsets.ModelViewSet):
    queryset = StatusInvoice.objects.all()
    serializer_class = StatusInvoiceSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def perform_create(self, serializer):
        # 1. الحصول على المستخدم من الطلب
        user = self.request.user
        
        # 2. البحث عن المتجر الذي يملكه هذا المستخدم
        # نستخدم first() لأنها ForeignKey (فقد يكون للمستخدم أكثر من متجر)
        shop = Shop.objects.filter(owner=user).first()
        
        if not shop:
            # سنقوم برفع خطأ إذا لم يكن للمستخدم متجر
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"error": "المستخدم الحالي لا يملك متجراً مسجلاً."})

        # 3. حفظ الفاتورة مع المتجر والمستخدم المكتشفين
        serializer.save(
            owner_user=user,
            created_user=user,
            shop=shop
        )

    def get_queryset(self):
        # تحسين: اجعل المستخدم يرى فقط فواتير متجره الخاص
        user = self.request.user
        if user.is_authenticated:
            return Invoice.objects.filter(shop__owner=user).select_related('shop', 'status').prefetch_related('items')
        return Invoice.objects.none()


class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
    
    def get_queryset(self):
        queryset = InvoiceItem.objects.all()
        
        # فلترة حسب الفاتورة
        invoice_id = self.request.query_params.get('invoice_id')
        if invoice_id:
            queryset = queryset.filter(invoice_id=invoice_id)
        
        return queryset.select_related('invoice', 'product')