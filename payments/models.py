from django.db import models

from invoices.models import Invoice

# Create your models here.


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class InvoicePayment(models.Model):
    invoice = models.ForeignKey('invoices.Invoice', on_delete=models.CASCADE)
    method = models.ForeignKey('payments.PaymentMethod', on_delete=models.CASCADE)
    amount = models.FloatField()
    paid_at = models.DateTimeField(auto_now_add=True)
    reference_number = models.CharField(max_length=255, blank=True, null=True)  # رقم مرجعي من مزود الخدمة


    def __str__(self):
        return f"{self.invoice} - {self.method} - {self.amount}"
