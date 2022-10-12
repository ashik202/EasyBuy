from django import forms
from .models import Coupon,UsedCoupons

class Couponform(forms.ModelForm):
    class Meta:
        model=Coupon
        fields=('coupon_name','coupon_code','amount')


class Couponusedform(forms.ModelForm):
    class Meta:
        model=UsedCoupons
        fields=('coupon','user')