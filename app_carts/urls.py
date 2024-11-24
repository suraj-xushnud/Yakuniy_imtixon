from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increment/<int:cart_item_id>/', views.increment_quantity, name='increment_quantity'),
    path('cart/decrement/<int:cart_item_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

]
