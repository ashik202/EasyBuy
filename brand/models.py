from django.db import models


# Create your models here.
class brand(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=224, blank=True)
    brand_image = models.ImageField(upload_to='photo/brand', blank=True)

    def __str__(self):
        return self.brand_name
