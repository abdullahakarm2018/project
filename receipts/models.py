from django.db import models

from invoices.models import Invoice
from shops.models import Shop
from django.conf import settings

# Create your models here.

class Receipt(models.Model):
    shop = models.ForeignKey(Shop,on_delete=models.PROTECT,blank=True,null=True)
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey('users.CustomUser',on_delete=models.PROTECT,blank=True,null=True, related_name="user_receipt")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note =models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return str(self.pk) + " | " + str(self.invoice)+ " | " + str(self.shop)