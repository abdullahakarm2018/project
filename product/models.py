from django.db import models
from django.conf import settings
from django.forms import ValidationError
# Create your models here.
class Category(models.Model):
    Type_Category = [("MA","Main"),("SU","Sub")]
    category_type =  models.CharField(max_length=5,choices=Type_Category)
    name = models.CharField(max_length=180 , blank=True)
    color = models.CharField(max_length=180 , blank=True)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey('users.CustomUser',on_delete=models.PROTECT,blank=True,null=True, related_name="created_category")
    updated_user = models.ForeignKey('users.CustomUser',on_delete=models.PROTECT,blank=True,null=True, related_name="updated_category")
    def __str__(self):
        return self.name

class Unit(models.Model):
    UNIT_TYPE_CHOICES = [
        ("MA", "Main"),
        ("SU", "Sub"),
    ]

    unit_type = models.CharField(max_length=5, choices=UNIT_TYPE_CHOICES)
    name = models.CharField(max_length=180, blank=True)
    parent_unit = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_units',
        limit_choices_to={'unit_type': 'MA'}  # فقط الوحدات الرئيسية يمكن اختيارها
    )
    note = models.CharField(max_length=180, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, blank=True, null=True, related_name="created_units")
    updated_user = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, blank=True, null=True, related_name="updated_units")

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=180 , blank=True)
    note = models.CharField(max_length=180 , blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    created_user = models.ForeignKey('users.CustomUser',on_delete=models.PROTECT,blank=True,null=True, related_name="created_company")
    updated_user = models.ForeignKey('users.CustomUser',on_delete=models.PROTECT,blank=True,null=True, related_name="updated_company")
    def __str__(self):
        return self.name

class PriceType(models.TextChoices):
    FIXED = 'fixed', 'ثابت'
    VARIABLE = 'variable', 'متغير'
class ProductType(models.TextChoices):
    Product = 'product', 'منتج'
    Service = 'service', 'خدمة'
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="product", null=True, blank=True)
    product_type = models.CharField(max_length=10, choices=ProductType.choices, default=ProductType.Product)
    price_type = models.CharField(max_length=10, choices=PriceType.choices, default=PriceType.FIXED)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    lessAmount = models.FloatField(blank=True, null=True, default=0)

    # علاقات الوحدة
    main_unit = models.ForeignKey(
        'Unit',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='main_unit_products',
        limit_choices_to={'unit_type': 'MA'}
    )
    sub_unit = models.ForeignKey(
        'Unit',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='sub_unit_products',
        limit_choices_to={'unit_type': 'SU'}
    )

    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True, null=True)
    barcode = models.CharField(max_length=180, blank=True, db_index=True,unique=True,
        null=True)
    package = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    note = models.CharField(max_length=180, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_user = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, blank=True, null=True, related_name="created_product")
    updated_user = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, blank=True, null=True, related_name="updated_product")
    is_global = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    created_by_shop = models.ForeignKey(
        'shops.Shop',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='private_products'
    )
    def __str__(self):
        return f"{self.name} | {self.product_type} | {self.id}"
    def clean(self):
        """
        التحقق من أن الوحدة الفرعية مرتبطة بالوحدة الرئيسية
        """
        if self.sub_unit and self.main_unit:
            if self.sub_unit.parent_unit != self.main_unit:
                raise ValidationError({
                    'sub_unit': 'الوحدة الفرعية يجب أن تكون تابعة للوحدة الرئيسية المختارة'
                })
        
    def save(self, *args, **kwargs):
        self.full_clean()  # يستدعي clean()
        super().save(*args, **kwargs)
