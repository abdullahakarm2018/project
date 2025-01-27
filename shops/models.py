from django.db import models
from users.models import Profile
from product.models import Product
# Create your models here.

class TypeShop(models.Model):
    name = models.CharField(max_length=180 , blank=True)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="created_typeShop")
    updated_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="updated_typeShop")
    def __str__(self):
        return self.name
class CategoryShop(models.Model):
    name = models.CharField(max_length=180 , blank=True)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="created_categoryShop")
    updated_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="updated_categoryShop")
    def __str__(self):
        return self.name
    
class Shop(models.Model):
   
    user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="user_shop")
    nameAr = models.CharField(max_length=150,null=True,blank=True)
    nameEn = models.CharField(max_length=150,null=True,blank=True)
    logo = models.ImageField( upload_to="shop", null=True,blank=True)
    type_shop = models.ForeignKey(TypeShop,on_delete=models.PROTECT,blank=True,null=True)
    category =models.ForeignKey(CategoryShop,on_delete=models.PROTECT,blank=True,null=True)
    note = models.CharField(max_length=180 , blank=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    tal_number = models.CharField(max_length=20,null=True,blank=True)
    whatsapp = models.CharField(max_length=20,null=True,blank=True)
    twitter = models.CharField(max_length=20,null=True,blank=True)
    facebook = models.CharField(max_length=20,null=True,blank=True)
    instagram = models.CharField(max_length=20,null=True,blank=True)
    snapchat = models.CharField(max_length=20,null=True,blank=True)
    tiktok = models.CharField(max_length=20,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="created_shop")
    updated_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="updated_shop")
    def __str__(self):
        return str(self.nameAr) + " | " + str(self.nameEn)
    
class ProductShop(models.Model):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="created_productShop")
    updated_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="updated_productShop")
    def __str__(self):
        return str(self.shop) + " | " + str(self.product)
    
class CostomerShop(models.Model):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,blank=True,null=True)
    costomer = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="created_costomerShop")
    updated_user = models.ForeignKey(Profile,on_delete=models.PROTECT,blank=True,null=True, related_name="updated_costomerShop")
    def __str__(self):
        return str(self.shop) + " | " + str(self.costomer)