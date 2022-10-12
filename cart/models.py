import product as product
from django.db import models
from  product.models import product,Variation
from accounts.models import Account


# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True, null=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
class Cartitem(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True,)
    products=models.ForeignKey(product,on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variation,default=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)

    def sub_total(self):
        if self.products.new_price !=0:
            return self.products.new_price *self.quantity
        else:
            return self.products.price * self.quantity
    def __str__(self):
        return self.products.product_name


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=200, null=True)
    coupon_code = models.CharField(max_length=200, null=True)
    amount = models.IntegerField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.coupon_name


class UsedCoupons(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE)
