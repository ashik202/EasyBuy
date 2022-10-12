from django import forms
from .models import BrandOffer,CategoryOffer,ProductOffer



class BrandOfffer_form(forms.ModelForm):
    class Meta:
        model=BrandOffer
        fields=('brand_name','discount',)


class CategoryOffer_form(forms.ModelForm):
    class Meta:
        model=CategoryOffer
        fields=('category_name','discount',)


class ProductOffer_form(forms.ModelForm):
    class Meta:
        model=ProductOffer
        fields=('product_name','discount',)