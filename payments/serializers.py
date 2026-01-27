# payments/serializers.py
from rest_framework import serializers
from .models import InvoicePayment

class InvoicePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoicePayment
        fields = '__all__'
