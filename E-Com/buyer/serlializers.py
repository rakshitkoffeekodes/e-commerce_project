from django.db.models import fields
from rest_framework import serializers
from .models import *


class BuyerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerRegistration
        fields = ("user_id", "user_firstname", "user_lastname", "user_address", "user_mobile_no", "user_password",
                  "user_email_id", "user_photo")

class BuyerCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerCart
        fields = '__all__'

class BuyerAddressSerializer(serializers.ModelSerializer):
    cart = ()

    class Meta:
        model = Checkout_details
        fields = '__all__'




class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = '__all__'
