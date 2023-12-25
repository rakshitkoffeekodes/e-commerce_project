from base.models import *
from base.models import Checkout_details
from django.db import models


# Create your models here.

class Register(models.Model):
    profile_picture = models.FileField(upload_to="media/", default="default.jpg")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(unique=True, max_length=10, default='+ 91')
    address = models.TextField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name


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
    product_images = models.JSONField()
    SKU = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
    product_price = models.IntegerField(blank=False)
    product_sale_price = models.IntegerField(blank=False)
    product_quantity = models.IntegerField(blank=False)
    product_category = models.CharField(max_length=50, choices=items)
    product_items = models.CharField(max_length=50, choices=sub_items)
    product_branding = models.CharField(max_length=50)
    product_tags = models.CharField(max_length=50)
    product_size = models.CharField(max_length=50)
    product_color = models.CharField(max_length=50)
    product_fabric = models.CharField(max_length=50)
    product_description = models.TextField()
    product_seller = models.ForeignKey(Register, on_delete=models.CASCADE)


# # ==================Check Out Details Model Table=====================
# class Details(models.Model):
#     firstname = models.CharField(max_length=50)
#     lastname = models.CharField(max_length=50)
#     country = models.CharField(max_length=25)
#     address = models.CharField(max_length=200)
#     second_address = models.CharField(max_length=200, null=True)
#     city = models.CharField(max_length=20)
#     state = models.CharField(max_length=25)
#     postcode = models.IntegerField(default=0)
#     phone = models.CharField(max_length=124)
#     email = models.CharField(max_length=50)
#     order = models.CharField(max_length=100, null=True)
#     cart = models.ForeignKey(BuyerCart, on_delete=models.CASCADE, null=True)
#     buyer = models.ForeignKey(BuyerRegistration, on_delete=models.CASCADE)

# def __str__(self):
#     return self.order


class Order(models.Model):
    cart = models.ForeignKey(Checkout_details, on_delete=models.CASCADE)
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


class Barcode(models.Model):
    code = models.CharField(max_length=100)
