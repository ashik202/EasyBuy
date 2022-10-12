from django.db import models
# Create your models here.
from brand.models import brand
from category.models import category
from product.models import product


class BrandOffer(models.Model):
    brand_name = models.OneToOneField(brand, on_delete=models.CASCADE)
    discount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_valid = models.BooleanField(default=True)

    def __int__(self):
        return self.brand_name


class CategoryOffer(models.Model):
    category_name = models.OneToOneField(category, on_delete=models.CASCADE)
    discount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_valid = models.BooleanField(default=True)

    def __int__(self):
        return self.category_name


class ProductOffer(models.Model):
    product_name = models.OneToOneField(product, on_delete=models.CASCADE)
    discount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_valid = models.BooleanField(default=True)

    def __int__(self):
        return self.product_name
from django.db import models

# Create your models here.
