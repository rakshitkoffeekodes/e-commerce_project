from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class AcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accept
        fields = '__all__'


class CancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancel
        fields = '__all__'
