from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    register_user = UserSerializer()

    class Meta:
        model = Register
        fields = ['profile_picture', 'mobile_no', 'address', 'register_user']


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
