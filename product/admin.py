from django.contrib import admin
from product.models import *
from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from .models import Product, Category, Unit, Company
from shops.models import Shop
# Register your models here.



# تخصيص كيفية قراءة البيانات من الإكسل
class ProductResource(resources.ModelResource):
    # ربط الحقول الخارجية بالأسماء بدلاً من الـ IDs
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')) # يفترض أن الموديل Category فيه حقل اسمه name
    
    main_unit = fields.Field(
        column_name='main_unit',
        attribute='main_unit',
        widget=ForeignKeyWidget(Unit, 'name'))
    
    sub_unit = fields.Field(
        column_name='sub_unit',
        attribute='sub_unit',
        widget=ForeignKeyWidget(Unit, 'name'))

    class Meta:
        model = Product
        # الحقول التي ستظهر في ملف الإكسل
        fields = ('id', 'name', 'barcode', 'price', 'package', 'category', 'main_unit', 'sub_unit', 'note')
        # تحديد الباركود كحقل فريد لتجنب تكرار المنتجات عند الرفع مرة أخرى
        import_id_fields = ('barcode',) 

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'barcode', 'price', 'category', 'is_approved')
    list_filter = ('category', 'is_approved', 'product_type')
    search_fields = ('name', 'barcode')
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Company)
admin.site.register(Product)