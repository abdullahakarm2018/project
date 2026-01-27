from django.db import models
from django.conf import settings 
from shops.models import Shop,CustomerShop,ProductShop
# Create your models here.
class StatusInvoice(models.Model):
    name = models.CharField(max_length=180 , blank=True)
    def __str__(self):
        return str(self.name) 
class Invoice(models.Model):
    owner_user = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, related_name='owned_invoices',blank=True,null=True)
    counterparty_user = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, related_name='counterparty_invoices',blank=True,null=True)
    shop = models.ForeignKey(Shop,on_delete=models.PROTECT,blank=True,null=True)
    status =models.ForeignKey(StatusInvoice,on_delete=models.PROTECT,blank=True,null=True)
    comments = models.TextField(default='', blank=True, null=True)
    total =models.DecimalField(max_digits=12, decimal_places=2, default=0)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey('users.CustomUser',on_delete=models.PROTECT,blank=True,null=True, related_name="created_invoices")
    updated_user = models.ForeignKey('users.CustomUser',on_delete=models.PROTECT,blank=True,null=True, related_name="updated_invoices")
    def __str__(self):
        return str(self.pk) + " | " + str(self.shop)+ " | " + str(self.counterparty_user)+ " | " + str(self.status)
    
    def calculate_total(self):
        """حساب المجموع الكلي للفاتورة من عناصرها"""
        total = sum(item.line_total for item in self.items.all())
        self.total = total
        self.save()
        return total
  
class InvoiceItem(models.Model):    
    invoice = models.ForeignKey(  # إصلاح: إعادة تسمية من 'invoiceId' وإصلاح related_name
        Invoice,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="items"  # إضافة: أفضل للوصول العكسي
    )
    product = models.ForeignKey(  # إصلاح: إعادة تسمية من 'productId'
        ProductShop,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note =models.CharField(max_length=180 , blank=True)
    def __str__(self):
        return str(self.invoice) + " | " + str(self.product)
    
    @property
    def line_total(self):
        return self.quantity * self.price