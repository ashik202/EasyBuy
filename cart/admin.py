from django.contrib import admin

# Register your models here.
from cart.models import Cart,Cartitem,Coupon,UsedCoupons

admin.site.register(Cart)
admin.site.register(Cartitem)
admin.site.register(Coupon)
admin.site.register(UsedCoupons)