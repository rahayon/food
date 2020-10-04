from django.db import models
from django.urls import reverse


class Category(models.Model):

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})




# Create your models here.
class Product(models.Model):

    title = models.CharField(max_length=264)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    short_description = models.CharField(max_length=264)
    full_description = models.TextField()
    feature_image = models.ImageField(upload_to='Products')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    old_price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("prdocuts_detail", kwargs={"pk": self.pk})

class ProductThumbnailImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_thumbnail')
    image = models.ImageField(upload_to='Products')

    class Meta:
        verbose_name = "ProductThumbnailImage"
        verbose_name_plural = "ProductThumbnailImages"

    

    def get_absolute_url(self):
        return reverse("ProductThumbnailImage_detail", kwargs={"pk": self.pk})
