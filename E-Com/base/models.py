from django.db import models
from seller.models import *


# Create your models here.
class BuyerRegistration(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_firstname = models.CharField(max_length=255)
    user_lastname = models.CharField(max_length=255)
    user_address = models.TextField(max_length=255)
    user_photo = models.FileField(default='defult.jpg', upload_to='buyer/', null=True)
    user_mobile_no = models.CharField(max_length=12, unique=True)
    user_email_id = models.CharField(max_length=255, unique=True)
    user_password = models.CharField(max_length=16)

    def __str__(self):
        return self.user_firstname + " " + self.user_lastname


class BuyerCart(models.Model):
    product = models.ForeignKey("seller.Product", on_delete=models.CASCADE, null=True)
    buyer = models.ForeignKey(BuyerRegistration, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    product_color = models.CharField(max_length=50, null=True)
    product_size = models.CharField(max_length=50, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.buyer)


class Checkout_details(models.Model):
    address = models.AutoField(primary_key=True, default=None)
    buyer = models.ForeignKey(BuyerRegistration, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(BuyerCart, on_delete=models.CASCADE, null=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    city = models.CharField(max_length=100)

    SELECT_STATE = (
        ('State Name', 'Andhra Pradesh'), ('State Name', 'Arunachal Pradesh'), ('State Name', 'Assam'),
        ('State Name', 'Bihar'), ('State Name', 'Chhattisgarh'), ('State Name', 'Goa'),
        ('State Name', 'Gujarat'), ('State Name', 'Haryana'), ('State Name', 'Himachal Pradesh'),
        ('State Name', 'Jharkhand'), ('State Name', 'Karnataka'), ('State Name', 'Kerala'),
        ('State Name', 'Madhya Pradesh'), ('State Name', 'Maharashtra'), ('State Name', 'Manipur'),
        ('State Name', 'Meghalaya'), ('State Name', 'Mizoram'), ('State Name', 'Nagaland'),
        ('State Name', 'Odisha'), ('State Name', 'Punjab'), ('State Name', 'Rajasthan'),
        ('State Name', 'Sikkim'), ('State Name', 'Tamil Nadu'), ('State Name', 'Telangana'),
        ('State Name', 'Tripura'), ('State Name', 'Uttar Pradesh'), ('State Name', 'Uttarakhand'),
        ('State Name', 'West Bengal'), ('State Name', 'Andaman and Nicobar Islands'), ('State Name', 'Chandigarh'),
        ('State Name', 'Dadra & Nagar Haveli and Daman & Diu'), ('State Name', 'Delhi'),
        ('State Name', 'Jammu and Kashmir'),
        ('State Name', 'Lakshadweep'), ('State Name', "Pondicherry"), ('State Name', "Ladakh"),
    )
    select_state = models.CharField(max_length=40, choices=SELECT_STATE)
    ord_rec_name = models.CharField(max_length=255)
    ord_rec_mobile_no = models.CharField(max_length=12)
    status = models.BooleanField(default=True)
    def __str__(self):
        return str(self.buyer)


class Payment(models.Model):
    order = models.CharField(max_length=100)
    cart = models.ForeignKey(BuyerCart, on_delete=models.CASCADE, null=True)
    buyer = models.ForeignKey(BuyerRegistration, on_delete=models.CASCADE)
    details = models.ForeignKey(Checkout_details, on_delete=models.CASCADE)

    def __str__(self):
        return self.order


class Return(models.Model):
    buyer = models.ForeignKey(BuyerRegistration, on_delete=models.CASCADE)
    order = models.ForeignKey(Payment, on_delete=models.CASCADE)
    returns = models.CharField(max_length=100)
    order_return_message = models.CharField(max_length=100, null='N/A')
    return_shipping_Fee = models.IntegerField(default=0)
    return_date = models.DateTimeField(null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.order)


class BuyerFeedback(models.Model):
    feedback_id = models.AutoField(primary_key=True, null=False)
    feedback_login = models.ForeignKey(BuyerRegistration, on_delete=models.CASCADE)
    feedback_product = models.ForeignKey("seller.Product", on_delete=models.CASCADE, null=True)
    feedback_description = models.TextField(max_length=500)
    feedback_datetime = models.DateTimeField(auto_now_add=True)
    feedback_rating = models.IntegerField()
    feedback_photo = models.FileField(upload_to='buyer/', null=True)

    def __str__(self):
        return str(self.feedback_login)
