from django.contrib import admin
from .models import *


<<<<<<< HEAD
@admin.register(BuyerRegistration)
class BuyerRegistrationadmin(admin.ModelAdmin):
    list_display = ['user', 'user_address', 'user_mobile_no', 'user_photo', 'buyer']
=======
class BuyerRegistrationadmin(admin.ModelAdmin):
    list_display = ('user', 'user_address', 'user_mobile_no', 'user_photo', 'buyer')

>>>>>>> 2d4d80ad731024b1962777daa941ef1894308664


@admin.register(BuyerCheckout_details)
class BuyerAddressadmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ["address", "street_address", "apartment_address", "pincode", "city", "select_state", "ord_rec_name",
                    "ord_rec_mobile_no", "buyer"]
=======
    list_display = ("address", "street_address", "apartment_address", "pincode", "city", "select_state", "ord_rec_name",
                    "ord_rec_mobile_no", "buyer")
>>>>>>> 2d4d80ad731024b1962777daa941ef1894308664


@admin.register(BuyerCart)
class BuyerCartadmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ["Cart", "buyer", "product", "qty", "date_added", "total"]
=======
    list_display = ("Cart", "buyer", "product", "qty", "date_added", "total")

>>>>>>> 2d4d80ad731024b1962777daa941ef1894308664


@admin.register(BuyerPurchase)
class BuyerPurchaseadmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ["purchase", "buyer", "qty", "product", "total", "cart", "checkout"]
=======
    list_display = ("purchase", "buyer", "qty", "product", "total", "cart", "checkout")
>>>>>>> 2d4d80ad731024b1962777daa941ef1894308664


@admin.register(BuyerFeedback)
class BuyerFeedbackadmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ["feedback", "feedback_description", "feedback_datetime", "feedback_rating", "feedback_photo",
                    "feedback_product", "feedback_login"]

=======
    list_display = (
        "feedback", "feedback_description", "feedback_datetime", "feedback_rating", "feedback_photo",
        "feedback_product",
        "feedback_login")
>>>>>>> 2d4d80ad731024b1962777daa941ef1894308664

@admin.register(BuyerPayment)
class BuyerPaymentadmin(admin.ModelAdmin):
    list_display = ["payment", "status", "amount", "currency", "order", "payment_intent_id", "created_at",
                    "updated_at", "cancel", "details", "buyer"]

<<<<<<< HEAD

@admin.register(BuyerReturn)
class Returnadmin(admin.ModelAdmin):
    list_display = ["order_return", "returns", "order_return_message", "return_shipping_Fee", "return_date", "status",
                    "buyer", "order"]

#
=======
admin.site.register(BuyerRegistration, BuyerRegistrationadmin)
admin.site.register(Buyer_checkout_details, BuyerAddressadmin)
admin.site.register(BuyerCart, BuyerCartadmin)
admin.site.register(BuyerPurchase, BuyerPurchaseadmin)
admin.site.register(BuyerPayment)
admin.site.register(BuyerFeedback, BuyerFeedbackadmin)
admin.site.register(Return)
>>>>>>> 2d4d80ad731024b1962777daa941ef1894308664
