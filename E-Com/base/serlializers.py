from django.db.models import fields
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    buyer = UserSerializer()

    class Meta:
        model = BuyerRegistration
        fields = ['buyer', 'user_photo', 'user_mobile_no', 'user_id']
        # fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email']
#
#
#
# class RegisterSerializer(serializers.ModelSerializer):
#     register_user = UserSerializer()
#
#     class Meta:
#         model = BuyerRegistration
#         fields = ['buyer', 'user_address', 'user_photo', 'user_mobile_no']


class BuyerCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerCart
        fields = '__all__'


class BuyercartPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerPurchase
        fields = '__all__'


class BuyerPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerPurchase
        fields = ("id", "total", "qty", "product", "buyer", "checkout")


class BuyerAddressSerializer(serializers.ModelSerializer):
    cart = ()

    class Meta:
        model = Checkout_details
        fields = '__all__'


class BuyerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerFeedback
        fields = '__all__'


class BuyerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerPayment
        fields = '__all__'


class BuyerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerOrder
        fields = '__all__'


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = '__all__'
