from django import forms
from payment.models import BillingAddress

class BillingForm(forms.ModelForm):
    
    class Meta:
        model = BillingAddress
        fields = ('address', 'postcode', 'city', 'country',)
