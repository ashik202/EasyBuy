

import admin_thumbnails
from django.apps import apps

from django.db import models
from django.db.models import Sum
from django.utils import timezone

from category.models import category
from brand.models import brand
import uuid
from django.urls import reverse

# Create your models here.
class product(models.Model):
    product_name=models.CharField(max_length=200,default='')
    product_model=models.CharField(max_length=50,default='')
    slug=models.SlugField(max_length=500,unique=True,default=uuid.uuid1)
    description=models.TextField(max_length=50)
    ram=models.TextField(max_length=50)
    Screensize=models.TextField(max_length=200)
    processor=models.TextField(max_length=100)
    storage=models.TextField(max_length=100)
    price=models.IntegerField()
    stock=models.IntegerField()
    image1 = models.ImageField(upload_to='photo/storetem',default='')
    image2 = models.ImageField(upload_to='photo/storetem',default='')
    image3 = models.ImageField(upload_to='photo/storetem',default='')
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    brand = models.ForeignKey(brand, on_delete=models.CASCADE)
    is_available=models.BooleanField(default=True)
    new_price=models.IntegerField(default=0)
    discount=models.CharField(max_length=100,default=0)
    def get_url(self):
        return reverse('single_product',args=[self.category.slug,self.slug])
    def __str__(self):
        return self.product_name

    def Offer_Price(self):
        try:
            if self.productoffer.is_valid:
                offer_price = (self.price * self.productoffer.discount) / 100
                new_price = self.price - offer_price
                return {
                    "new_price": new_price,
                    "discount": self.productoffer.discount,
                }
            raise
        except:
            try:
                if self.brand_name.brandoffer.is_valid:
                    offer_price = (
                                          self.price * self.brand_name.brandoffer.discount
                                  ) / 100
                    new_price = self.price - offer_price
                    return {
                        "new_price": new_price,
                        "discount": self.brand_name.brandoffer.discount,
                    }
                raise
            except:
                try:
                    if self.category.categoryoffer.is_valid:
                        offer_price = (
                                              self.price * self.category.categoryoffer.discount
                                      ) / 100
                        new_price = self.price - offer_price
                        return {
                            "new_price": new_price,
                            "discount": self.category.categoryoffer.discount,
                        }
                    raise
                except:
                    pass

    def get_revenue(self, month=timezone.now().month):
        orderproduct = apps.get_model("orders", "OrderProduct")
        orders = orderproduct.objects.filter(
            product=self, created_at__month=month,
        )
        return orders.values("product").annotate(revenue=Sum("product_price"))

    def get_profit(self, month=timezone.now().month):
        orderproduct = apps.get_model("orders", "OrderProduct")
        orders = orderproduct.objects.filter(
            product=self, created_at__month=month
        )
        profit_calculted = orders.values("product").annotate(
            profit=Sum("product_price")
        )


        return  profit_calculted

    def get_count(self, month=timezone.now().month):
        orderproduct = apps.get_model("orders", "OrderProduct")
        orders = orderproduct.objects.filter(
            product=self, created_at__month=month
        )
        return orders.values("product").annotate(quantity=Sum("quantity"))


class VariationManger(models.Manager):
    def Colors(self):
        return super(VariationManger, self).filter(variation_category='color',is_active=True)



variation_category_choice=(('color','color'),)

class Variation(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)
    objects=VariationManger()
    def __str__(self):
        return self.variation_value



class ProductGallery(models.Model):
    product=models.ForeignKey(product,default=None,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='store/products',max_length=225)
    def __str__(self):
        return self.product.product_name

