from django.contrib import admin
from product.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Company)
admin.site.register(Product)