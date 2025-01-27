from django.db import models
from users.models import Profile
# Create your models here.
class Category(models.Model):
    Type_Category = [("MA","Main"),("SU","Sub")]
    category_type =  models.CharField(max_length=5,choices=Type_Category)
    name = models.CharField(max_length=180 , blank=True)
    color = models.CharField(max_length=180 , blank=True)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="created_category")
    updated_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="updated_category")
    def __str__(self):
        return self.name

class Unit(models.Model):
    Type_unit = [("MA","Main"),("SU","Sub")]
    unit_type =  models.CharField(max_length=5,choices=Type_unit)
    name = models.CharField(max_length=180 , blank=True)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="created_unit")
    updated_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="updated_unit")
    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=180 , blank=True)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="created_company")
    updated_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="updated_company")
    def __str__(self):
        return self.name
class PriceType(models.Model):
    name = models.CharField(max_length=180 , blank=True)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="created_price_type")
    updated_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="updated_price_type")
    def __str__(self):
        return self.name
    
class Product(models.Model):
    Type_Product = [("SE","Service"),("PR","Product")]
    name = models.CharField(max_length=15,null=True,blank=True)
    image = models.ImageField( upload_to="product", null=True,blank=True)
    product_type = models.CharField(max_length=5,choices=Type_Product)
    price_type =models.ForeignKey(PriceType,on_delete=models.PROTECT,blank=True,null=True)
    lessAmount = models.FloatField(blank=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,blank=True,null=True)
    unit = models.ForeignKey(Unit,on_delete=models.PROTECT, blank=True,null=True)
    company = models.ForeignKey(Company,on_delete=models.PROTECT, blank=True,null=True)
    barcode = models.CharField(max_length=180 , blank=True)
    package = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="created_product")
    updated_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="updated_product")
    def __str__(self):
        return str(self.name) + " | " + str(self.product_type)