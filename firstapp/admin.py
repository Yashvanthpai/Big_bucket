from django.contrib import admin

# Register your models here.
from firstapp import models

admin.site.register(models.Product)
admin.site.register(models.cart)
admin.site.register(models.order)