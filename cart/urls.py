from django.urls import path, include
from cart import views

urlpatterns = [
    path('', views.cart, name='cartpage'),
    path('addcart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('removecart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('removecartitem/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('coupon/', views.couponapply, name='coupon')

]
