from django.contrib import admin
from .models import *

# Register your models here.
class BuyerRegistrationadmin(admin.ModelAdmin):
    list_display = ("user_id", "user_firstname", "user_lastname", "user_address", "user_mobile_no", "user_password","user_email_id","user_photo")

class BuyerAddressadmin(admin.ModelAdmin):
    list_display = ("address_id","street_address", "apartment_address", "pincode", "city", "select_state", "ord_rec_name",
                  "ord_rec_mobile_no")

class BuyerCartadmin(admin.ModelAdmin):
    list_display = ("buyer","qty", "date_added", "total", "product")



admin.site.register(BuyerRegistration,BuyerRegistrationadmin)
admin.site.register(BuyerAddress,BuyerAddressadmin)
admin.site.register(BuyerCart,BuyerCartadmin)