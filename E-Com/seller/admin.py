from django.contrib import admin
from .models import *


# Register your models here.

class register(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'password', 'mobile_no', 'address')


class product(admin.ModelAdmin):
    list_display = (
        'id', 'SKU', 'product_name', 'product_price', 'product_sale_price', 'product_quantity', 'product_category',
        'product_items', 'product_branding', 'product_tags', 'product_size', 'product_color', 'product_fabric',
        'product_seller')


# class details(admin.ModelAdmin):
#     list_display = ('id', 'order', 'cart_id', 'buyer')


class order(admin.ModelAdmin):
    list_display = ('id', 'cart', 'order', 'product', 'buyer', 'status')


class accept(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'buyer', 'status')


admin.site.register(Register, register)
admin.site.register(Product, product)
# admin.site.register(Details, details)
admin.site.register(Order, order)
admin.site.register(Accept, accept)
admin.site.register(Cancel)
admin.site.register(Barcode)
