from django.contrib import admin
from .models import PaymentMethod, InvoicePayment
# Register your models here.




@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(InvoicePayment)
class InvoicePaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'method', 'amount', 'paid_at')
    list_filter = ('method', 'paid_at')
