from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "phone", "message")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Атыңыз"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Телефон (міндетті емес)"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Хабарламаңыз немесе пікіріңіз..."}),
        }
