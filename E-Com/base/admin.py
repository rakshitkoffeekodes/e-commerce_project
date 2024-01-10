from django.contrib import admin
from .models import *


@admin.register(BuyerRegistration)
class BuyerRegistrationadmin(admin.ModelAdmin):
    list_display = ['user', 'user_address', 'user_mobile_no', 'user_photo', 'buyer']


@admin.register(BuyerCheckout_details)
class BuyerAddressadmin(admin.ModelAdmin):
    list_display = ["address", "street_address", "apartment_address", "pincode", "city", "select_state", "ord_rec_name",
                    "ord_rec_mobile_no", "buyer"]


@admin.register(BuyerCart)
class BuyerCartadmin(admin.ModelAdmin):
    list_display = ["Cart", "buyer", "product", "qty", "date_added", "total"]


@admin.register(BuyerPurchase)
class BuyerPurchaseadmin(admin.ModelAdmin):
    list_display = ["purchase", "buyer", "qty", "product", "total", "cart", "checkout"]


@admin.register(BuyerFeedback)
class BuyerFeedbackadmin(admin.ModelAdmin):
    list_display = ["feedback", "feedback_description", "feedback_datetime", "feedback_rating", "feedback_photo",
                    "feedback_product", "feedback_login"]


@admin.register(BuyerPayment)
class BuyerPaymentadmin(admin.ModelAdmin):
    list_display = ["payment", "status", "amount", "currency", "order", "payment_intent_id", "created_at",
                    "updated_at", "cancel", "details", "buyer"]


@admin.register(BuyerReturn)
class Returnadmin(admin.ModelAdmin):
    list_display = ["order_return", "returns", "order_return_message", "return_shipping_Fee", "return_date", "status",
                    "buyer", "order"]

#
