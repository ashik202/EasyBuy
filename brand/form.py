from django import forms
from .models import brand

class brandform(forms.ModelForm):
    class Meta:
        model=brand
        fields=('brand_name','slug','description','brand_image')