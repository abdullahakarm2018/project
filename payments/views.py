from django.shortcuts import render

# Create your views here.
# payments/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import InvoicePayment
from .serializers import InvoicePaymentSerializer

class InvoicePaymentsView(APIView):
    def get(self, request, invoice_id):
        payments = InvoicePayment.objects.filter(invoice__id=invoice_id)
        serializer = InvoicePaymentSerializer(payments, many=True)
        return Response(serializer.data)
