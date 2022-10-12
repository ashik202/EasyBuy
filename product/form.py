from django import forms
from .models import product,Variation

class productform(forms.ModelForm):
    class Meta:
        model=product
        fields=('product_name','product_model','slug','description','ram','Screensize','processor','storage','price','stock','image1','image2','image3','category','brand')


class variationform(forms.ModelForm):
    class Meta:
        model=Variation
        fields=('product','variation_category','variation_value')