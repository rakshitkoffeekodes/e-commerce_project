from django.contrib import admin
from .models import *


# Register your models here.
class BuyerRegistrationadmin(admin.ModelAdmin):
    list_display = (
        "user_id",  "user_address", "user_mobile_no", "user_photo","buyer")


class BuyerAddressadmin(admin.ModelAdmin):
    list_display = ("street_address", "apartment_address", "pincode", "city", "select_state", "ord_rec_name",
                    "ord_rec_mobile_no")


class BuyerCartadmin(admin.ModelAdmin):
    list_display = ("buyer", "product", "qty", "date_added", "total")

class BuyerPurchaseadmin(admin.ModelAdmin):
    list_display = ("buyer", "qty", "product", "total","cart","checkout")

# BuyerFeedback


class BuyerFeedbackadmin(admin.ModelAdmin):
    list_display = ("feedback_id", "feedback_description", "feedback_datetime", "feedback_rating","feedback_photo","feedback_product","feedback_login")

class BuyerOrderadmin(admin.ModelAdmin):
    list_display = ("order", "order_number", "customer_name", "product_name","order_date","amount","buyer")


admin.site.register(BuyerRegistration, BuyerRegistrationadmin)
admin.site.register(Checkout_details, BuyerAddressadmin)
admin.site.register(BuyerCart, BuyerCartadmin)
admin.site.register(BuyerPurchase, BuyerPurchaseadmin)
admin.site.register(BuyerPayment)
admin.site.register(BuyerFeedback, BuyerFeedbackadmin)
admin.site.register(BuyerOrder, BuyerOrderadmin)
admin.site.register(Return)
