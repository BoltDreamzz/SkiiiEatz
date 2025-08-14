from django import forms
from .models import Vendor, Business, PayoutRequest

class VendorSignupForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['business_name', 'phone', 'address']
    business_type = forms.ChoiceField(choices=Business.BUSINESS_TYPES, required=True)

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['business_type', 'description', 'logo']

class PayoutRequestForm(forms.ModelForm):
    class Meta:
        model = PayoutRequest
        fields = ['amount']
