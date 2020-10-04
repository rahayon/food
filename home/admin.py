from django.contrib import admin

# Register your models here.
from home.models import Category, Product, ProductThumbnailImage


class ProductThumbnailImageAdmin(admin.StackedInline):
    model = ProductThumbnailImage

 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductThumbnailImageAdmin]
 
    class Meta:
       model = Product
 

admin.site.register(Category)
