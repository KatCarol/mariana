from django.contrib import admin

from dashboard.models import Batch, Drug, ProductCategory, Stock

# Register your models here.
admin.site.register(Drug)
admin.site.register(Stock)
admin.site.register(Batch)
admin.site.register(ProductCategory)