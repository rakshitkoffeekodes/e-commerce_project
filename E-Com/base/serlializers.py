from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class BuyerRegistrationSerializer(serializers.ModelSerializer):
    buyer = UserSerializer()

    class Meta:
        model = BuyerRegistration
        fields = ['user', 'user_address', 'user_photo', 'user_mobile_no', 'buyer']


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
        model = Buyer_checkout_details
        fields = '__all__'


class BuyerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerFeedback
        fields = '__all__'


class BuyerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerPayment
        fields = '__all__'


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = '__all__'
