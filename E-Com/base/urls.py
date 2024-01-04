from django.urls import path

from . import views


urlpatterns = [
    path("user_registration", views.user_registration, name="user_registration"),
    path("user_login", views.user_login, name="user_login"),
    path("user_profile", views.user_profile, name="user_profile"),
    path("user_update", views.user_update, name="user_update"),
    path("user_search_product", views.user_search_product, name="user_search_product"),
    path("user_view_product", views.user_view_product, name="user_view_product"),
    path("user_insert_address", views.user_insert_address, name="user_insert_address"),
    path("user_view_address", views.user_view_address, name="user_view_address"),
    path("user_update_address", views.user_update_address, name="user_update_address"),
    path("user_delete_address", views.user_delete_address, name="user_delete_address"),
    path("user_insert_cart", views.user_insert_cart),
    path("user_view_cart", views.user_view_cart, name="user_view_cart"),
    path("user_update_cart", views.user_update_cart, name="user_update_cart"),
    path("user_delete_cart", views.user_delete_cart, name="user_delete_cart"),
    path("user_insert_buynow", views.user_insert_buynow, name="user_insert_buynow"),
    path("user_insert_cart_buynow", views.user_insert_cart_buynow, name="user_insert_cart_buynow"),
    path("user_filter_product", views.user_filter_product, name="user_filter_product"),
    path("user_insert_feedback", views.user_insert_feedback, name="user_insert_feedback"),
    path("user_view_feedback", views.user_view_feedback, name="user_view_feedback"),
    path("create_payment_intent", views.create_payment_intent, name="create_payment_intent"),
    path("payment_intent", views.payment_intent, name="payment_intent"),
    path("stripe_config", views.stripe_config, name="stripe_config"),

]