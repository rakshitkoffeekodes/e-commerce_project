from django.db.models import fields
from rest_framework import serializers
from .models import *
import datetime


class BuyerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerRegistration
        fields = ("user_id", "user_firstname", "user_lastname", "user_address", "user_mobile_no", "user_password",
                  "user_email_id", "user_photo")


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


def check_expiry_month(value):
    if not 1 <= int(value) <= 12:
        raise serializers.ValidationError("Invalid expiry month.")


def check_expiry_year(value):
    today = datetime.datetime.now()
    if not int(value) >= today.year:
        raise serializers.ValidationError("Invalid expiry year.")


def check_cvc(value):
    if not 3 <= len(value) <= 4:
        raise serializers.ValidationError("Invalid cvc number.")


def check_payment_method(value):
    payment_method = value.lower()
    if payment_method not in ["card"]:
        raise serializers.ValidationError("Invalid payment_method.")


class PaymentSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=150, required=True)
    expiry_month = serializers.CharField(max_length=150, required=True, validators=[check_expiry_month])
    expiry_year = serializers.CharField(max_length=150, required=True, validators=[check_expiry_year])
    cvc = serializers.CharField(max_length=150, required=True, validators=[check_cvc])
#

# class ReturnSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Return
#         fields = '__all__'
