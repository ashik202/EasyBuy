from django import forms
from .models import category

class categoryform(forms.ModelForm):
    class Meta:
        model=category
        fields=('category_name','slug','description','cat_image')