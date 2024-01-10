from django.contrib import admin
from .models import *


class BuyerRegistrationadmin(admin.ModelAdmin):
    list_display = ('user', 'user_address', 'user_mobile_no', 'user_photo', 'buyer')


class BuyerAddressadmin(admin.ModelAdmin):
    list_display = ("address", "street_address", "apartment_address", "pincode", "city", "select_state", "ord_rec_name",
                    "ord_rec_mobile_no", "buyer")


class BuyerCartadmin(admin.ModelAdmin):
    list_display = ("Cart", "buyer", "product", "qty", "date_added", "total")


class BuyerPurchaseadmin(admin.ModelAdmin):
    list_display = ("purchase", "buyer", "qty", "product", "total", "cart", "checkout")


class BuyerFeedbackadmin(admin.ModelAdmin):
    list_display = (
        "feedback", "feedback_description", "feedback_datetime", "feedback_rating", "feedback_photo",
        "feedback_product",
        "feedback_login")


admin.site.register(BuyerRegistration, BuyerRegistrationadmin)
admin.site.register(Buyer_checkout_details, BuyerAddressadmin)
admin.site.register(BuyerCart, BuyerCartadmin)
admin.site.register(BuyerPurchase, BuyerPurchaseadmin)
admin.site.register(BuyerPayment)
admin.site.register(BuyerFeedback, BuyerFeedbackadmin)
admin.site.register(Return)
