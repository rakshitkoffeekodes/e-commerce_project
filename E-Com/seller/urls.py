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
    path('view_order/', views.view_order),
    path('filter_order_date/', views.filter_order_date),
    path('filter_dispatch_date/', views.filter_dispatch_date),
    path('order_search/', views.order_search),
    path('order_accept/', views.order_accept),
    path('view_accept_order/', views.view_accept_order),
    path('order_label/', views.order_label),
]
