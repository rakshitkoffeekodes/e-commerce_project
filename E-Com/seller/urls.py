from django.urls import path
from seller import views

urlpatterns = [
    path('', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('profile/', views.profile),
    path('update_profile/', views.update_profile),
    path('add_product/', views.add_product),
    path('view_all_product/', views.view_all_product),
    path('update_product/', views.update_product),
    path('delete_product/', views.delete_product),
    path('pending_order/', views.pending_order),
    path('filter_order_date/', views.filter_order_date),
    path('filter_dispatch_date/', views.filter_dispatch_date),
    path('order_search/', views.order_search),
    path('order_accept/', views.order_accept),
    path('ready_to_ship/', views.ready_to_ship),
    path('shipping_label/', views.shipping_label),
    path('cancel_order/', views.cancel_order),
    path('cancelled/', views.cancelled),
    path('pricing/', views.pricing),
    path('edit_pricing/', views.edit_pricing),
    path('filter_category/', views.filter_category),
    path('date_growth/', views.date_growth),
]
