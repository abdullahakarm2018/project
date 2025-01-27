from django.db import models
from users.models import Profile
from shops.models import Shop,CostomerShop,ProductShop
# Create your models here.
class SatusInvoice(models.Model):
    name = models.CharField(max_length=180 , blank=True)
    def __str__(self):
        return str(self.invoice) + " | " + str(self.project)
class Invoice(models.Model):
    costomer = models.ForeignKey(CostomerShop,on_delete=models.PROTECT,blank=True,null=True, related_name="costomer_invoice")
    shop = models.ForeignKey(Shop,on_delete=models.PROTECT,blank=True,null=True)
    satus =models.ForeignKey(SatusInvoice,on_delete=models.PROTECT,blank=True,null=True)
    comments = models.TextField(default='', blank=True, null=True)
    total = models.FloatField(default=0)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="created_invoice")
    updated_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="updated_invoice")
    def __str__(self):
        return str(self.pk) + " | " + str(self.shop)+ " | " + str(self.costomer)+ " | " + str(self.satus)
  
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,blank=True,null=True)
    project = models.ForeignKey(ProductShop,on_delete=models.PROTECT,blank=True,null=True)
    quintity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note =models.CharField(max_length=180 , blank=True)
    def __str__(self):
        return str(self.invoice) + " | " + str(self.project)