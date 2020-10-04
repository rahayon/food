from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.
class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=264, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    

    class Meta:
        verbose_name = "BillingAddress"
        verbose_name_plural = "BillingAddresss"

    def __str__(self):
        return f'{self.user.profile.username} Billing Address'

    def get_absolute_url(self):
        return reverse("BillingAddress_detail", kwargs={"pk": self.pk})

    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]
        for field_name in field_names:
            value = getattr(self,field_name)
            if value is None or value == '':
                return False
        return True
