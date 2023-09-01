from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('main/menu/<slug:slug>/', views.main_menu_custom, name='main_menu_cat'),
    path('main/menu/', views.main_menu_custom, name='main_menu'),
    path('card/clear/', views.cart_clear, name='cart_clear'),
    path('card/add/', views.cart_add, name='cart_add'),
    path('card/remove/', views.cart_remove, name='cart_remove'),
    path('order/create/', views.order_create, name='order_create'),
]
