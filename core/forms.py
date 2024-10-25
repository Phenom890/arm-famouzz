from django import forms

from .models import Address, Refund, Contact

REGION_CHOICES = (
    ('AS', 'Ashanti'),
    ('GA', 'Accra'),
    ('WR', 'Western'),
    ('OR', 'Oti'),
    ('NR', 'Northern'),
    ('UW', 'Upper West'),
    ('UE', 'Upper East')
)


class AddressForm(forms.ModelForm):
    locality = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "eg. Aboabo",
        "aria-label": "Aboabo",
        "aria-describedby": "basic-addon1"
    }))
    street_name = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "eg. Sarkin Adarawa St",
        "aria-label": "Sarkin Adarawa St",
        "aria-describedby": "basic-addon1"
    }))
    region = forms.CharField(required=False, max_length=40, widget=forms.Select(attrs={
        "class": "form-control",
        "placeholder": "Ashanti",
        "aria-label": "Ashanti",
        "aria-describedby": "basic-addon1"
    }, choices=REGION_CHOICES))
    house_number = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "eg. PLT 7 BLK 7",
        "aria-label": "PLT 7 BLK 7",
        "aria-describedby": "basic-addon1"
    }))

    class Meta:
        model = Address
        fields = ['locality', 'street_name', 'region', 'house_number']


class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['reason']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['message']