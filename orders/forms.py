from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("cargo_type", "weight_kg", "description", "origin", "destination", "status")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

