from django.conf import settings
from django.db import models
from django.urls import reverse

from home.models import Product


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f'{self.quantity} x {self.item}'

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, '0.2f')
        return float_total

    

    def get_absolute_url(self):
        return reverse("Cart_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    paymentID = models.CharField(max_length=264, blank=True, null=True)
    orderID = models.CharField(max_length=264, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    served = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total

    
    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})
