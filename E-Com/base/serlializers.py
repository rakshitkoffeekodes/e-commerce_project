from django.db.models import fields
from rest_framework import serializers
from .models import *


class BuyerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerRegistration
        fields = ("user_id", "user_firstname", "user_lastname", "user_address", "user_mobile_no", "user_password",
                  "user_email_id", "user_photo")


class BuyerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout_details
        fields = (
            "address_id", "street_address", "apartment_address", "pincode", "city", "select_state", "ord_rec_name",
            "ord_rec_mobile_no")


class BuyerCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerCart
        fields = ("buyer", "qty", "date_added", "total", "product")
