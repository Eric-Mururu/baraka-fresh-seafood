from django import forms
from django.utils import timezone

from .models import OrderEnquiry


class OrderEnquiryForm(forms.ModelForm):
    class Meta:
        model = OrderEnquiry
        fields = [
            'customer_name', 'phone', 'email', 'customer_type', 'product',
            'quantity_kg', 'delivery_location', 'preferred_date', 'notes',
        ]
        labels = {
            'customer_name': 'Your name',
            'phone': 'Phone number',
            'email': 'Email address (optional)',
            'customer_type': 'Customer type',
            'product': 'Seafood product',
            'quantity_kg': 'Quantity (kg)',
            'delivery_location': 'Delivery location',
            'preferred_date': 'Preferred delivery or collection date',
            'notes': 'Additional instructions (optional)',
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'tel'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_type': forms.Select(attrs={'class': 'form-select'}),
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity_kg': forms.NumberInput(attrs={'class': 'form-control', 'min': 2, 'placeholder': 'Minimum 2'}),
            'delivery_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Watamu, Kilifi or collection'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_type'].choices = [('', 'Choose one')] + OrderEnquiry.CUSTOMER_TYPES
        self.fields['product'].choices = [('', 'Choose a product')] + OrderEnquiry.PRODUCTS

    def clean_preferred_date(self):
        date = self.cleaned_data['preferred_date']
        if date < timezone.localdate():
            raise forms.ValidationError('Please choose today or a later date.')
        return date