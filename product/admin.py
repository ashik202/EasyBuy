import admin_thumbnails
from django.contrib import admin
from .models import product,Variation,ProductGallery

# Register your models here.

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model =ProductGallery
    extra = 1
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')

admin.site.register(Variation,VariationAdmin)
admin.site.register(ProductGallery)
admin.site.register(product,ProductAdmin)
