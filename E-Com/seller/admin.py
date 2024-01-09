from django.contrib import admin
from .models import *


class register(admin.ModelAdmin):
    list_display = ('register_key', 'register_user', 'mobile_no', 'address')


class product(admin.ModelAdmin):
    list_display = (
        'product_key', 'product_SKU', 'product_name', 'product_price', 'product_sale_price', 'product_quantity', 'product_category',
        'product_sub_category', 'product_branding', 'product_tags', 'product_size', 'product_color', 'product_fabric',
        'product_seller')


class order(admin.ModelAdmin):
    list_display = ('order_key', 'details', 'order', 'product', 'buyer', 'status')


class accept(admin.ModelAdmin):
    list_display = ('accept_key', 'order', 'product', 'buyer', 'status')


class cancel(admin.ModelAdmin):
    list_display = ('cancel_key', 'order', 'product', 'buyer', 'status')


admin.site.register(Register, register)
admin.site.register(Product, product)
admin.site.register(Order, order)
admin.site.register(Accept, accept)
admin.site.register(Cancel, cancel)
