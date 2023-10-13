from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['address'].required = True
        self.fields['city'].required = True
        self.fields['postal_code'].required = True
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email',
            'address', 'city',  'postal_code'
        ]
