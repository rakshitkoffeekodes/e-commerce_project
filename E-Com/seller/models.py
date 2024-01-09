from django.contrib.auth.models import User

from base.models import *
from django.db import models


class Register(models.Model):
    register_key = models.AutoField(primary_key=True)
    register_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile_picture = models.FileField(upload_to="media/", default="default.jpg")
    mobile_no = models.CharField(unique=True, max_length=10, default='+ 91')
    address = models.TextField()

    def __str__(self):
        return str(self.register_user)


class Product(models.Model):
    items = (('CLOTHE', 'CLOTHE'), ('ELECTRONICS', 'ELECTRONICS'), ('BOOKS', 'BOOKS'),
             ('BEAUTY', 'BEAUTY'), ('MEN ACCESSORIES', 'MEN ACCESSORIES'), ('WOMEN ACCESSORIES', 'WOMEN ACCESSORIES'),
             ('FURNITURE', 'FURNITURE'), ('GARDEN', 'GARDEN'))
    sub_items = [
        ('CLOTHE', (('BOY', 'BOY'), ('GIRL', 'GIRL'), ('MEN', 'MEN'), ('WOMEN', 'WOMEN'))),
        ('ELECTRONICS', (('MOBILE', 'MOBILE'), ('LAPTOP', 'LAPTOP'), ('TABLET', 'TABLET'), ('COMPUTER', 'COMPUTER'),
                         ('TV', 'TV'), ('CAMERA', 'CAMERA'), ('HOME AUDIO', 'HOME AUDIO'))),
        ('BOOKS', (('FINANCE & ACCOUNTING EXAMS BOOKS', 'FINANCE & ACCOUNTING EXAMS BOOKS'),
                   ('GOVERNMENT EXAMS BOOKS', 'GOVERNMENT EXAMS BOOKS'),
                   ('EXAMS BY UPSC BOOKS', 'EXAMS BY UPSC BOOKS'),
                   ('ENGINEERING ENTRANCE BOOKS', 'ENGINEERING ENTRANCE BOOKS'), ('DEFENCE BOOKS', 'DEFENCE BOOKS'),
                   ('BANKING & INSURANCE BOOKS', 'BANKING & INSURANCE BOOKS'),
                   ('ARTS, DESIGN AND EDUCATION BOOKS', 'ARTS, DESIGN AND EDUCATION BOOKS'))),
        ('BEAUTY', (('MAKEUP', 'MAKEUP'), ('SKIN', 'SKIN'), ('HAIR', 'HAIR'), ('FRAGRANCES', 'FRAGRANCES'),
                    ('MENS GROOMING', 'MENS GROOMING'), ('UNISEX PERSONAL CARE', 'UNISEX PERSONAL CARE'))),
        ('MEN ACCESSORIES', (('BELT', 'BELT'), ('CAPS & HATS', 'CAPS & HATS'),
                             ('MUFFLERS, SCARVES & GLOVES', 'MUFFLERS, SCARVES & GLOVES'),
                             ('HANDKERCHIEFS', 'HANDKERCHIEFS'), ('SOCKS', 'SOCKS'),
                             ('SUNGLASSES', 'SUNGLASSES'), ('WALLET', 'WALLET'),
                             ('WATCHES', 'WATCHES'), ('HELMET', 'HELMET'))),
        ('WOMEN ACCESSORIES', (('JEWELLERY', 'JEWELLERY'), ('BELTS', 'BELTS'),
                               ('CAPS & HATS', 'CAPS & HATS'),
                               ('HAIR ACCESSORIES', 'HAIR ACCESSORIES'), ('SOCKS', 'SOCKS'),
                               ('SUNGLASSES', 'SUNGLASSES'), ('UMBRELLAS', 'UMBRELLAS'),
                               ('WATCHES', 'WATCHES'), ('PINS', 'PINS'))),
        ('FURNITURE', 'FURNITURE'),
        ('GARDEN', (('WATERING CANS', 'WATERING CANS'), ('GARDENING TOOLS', 'GARDENING TOOLS'),
                    ('HOSE NOZZLES', 'HOSE NOZZLES'), ('GARDEN FAUCETS', 'GARDEN FAUCETS'),
                    ('WATER PUMPS', 'WATER PUMPS'), ('GARDEN SPRAY', 'GARDEN SPRAY')))
    ]
    product_key = models.AutoField(primary_key=True)
    product_images = models.JSONField()
    product_SKU = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
    product_price = models.IntegerField(blank=False)
    product_sale_price = models.IntegerField(blank=False)
    product_quantity = models.IntegerField(blank=False)
    product_category = models.CharField(max_length=50, choices=items)
    product_sub_category = models.CharField(max_length=50, choices=sub_items)
    product_branding = models.CharField(max_length=50)
    product_tags = models.CharField(max_length=50)
    product_size = models.CharField(max_length=50)
    product_color = models.CharField(max_length=50)
    product_fabric = models.CharField(max_length=50)
    product_description = models.TextField()
    product_stock = models.CharField(max_length=20, default='Is Stock')
    product_date = models.DateTimeField(null=True)
    product = models.CharField(max_length=50, null=True)
    product_seller = models.ForeignKey(Register, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    order_key = models.AutoField(primary_key=True)
    details = models.ForeignKey(Checkout_details, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerRegistration, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    product_color = models.CharField(max_length=50)
    product_size = models.CharField(max_length=50)
    total = models.IntegerField(default=0)
    order = models.CharField(max_length=20, null=True)
    company = models.CharField(max_length=20)
    dispatch_date = models.DateTimeField()
    order_date = models.DateTimeField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.order)


class Accept(models.Model):
    accept_key = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerRegistration, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    product_color = models.CharField(max_length=50)
    product_size = models.CharField(max_length=50)
    total = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.order)


class Cancel(models.Model):
    cancel_key = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerRegistration, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    product_color = models.CharField(max_length=50)
    product_size = models.CharField(max_length=50)
    total = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.order)
