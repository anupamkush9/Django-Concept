from django.contrib import admin
from .models import Order, Product

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'paid', 'amount', 'description']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'updated_at', 'description']

admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
