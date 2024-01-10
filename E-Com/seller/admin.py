from django.contrib import admin
from .models import *
from django.contrib import admin
from .models import Product

# Register your models here.

class register(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'mobile_no', 'address')


class product(admin.ModelAdmin):
    list_display = (
        'id', 'SKU', 'product_name', 'product_price', 'product_sale_price', 'product_quantity', 'product_category',
        'product_sub_category', 'product_branding', 'product_tags', 'product_size', 'product_color', 'product_fabric',
        'product_seller','product_stock')





class order(admin.ModelAdmin):
    list_display = ('id', 'details', 'order', 'product', 'buyer', 'status')


class accept(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'buyer', 'status')


admin.site.register(Register, register)
admin.site.register(Product, product)
admin.site.register(Order, order)
admin.site.register(Accept, accept)
admin.site.register(Cancel)
