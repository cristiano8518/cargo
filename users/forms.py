from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Email")
    phone = forms.CharField(max_length=20, required=False, label="Телефон")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if "class" not in (field.widget.attrs or {}):
                field.widget.attrs["class"] = "form-control"
        self.fields["username"].label = "Логин"
        self.fields["username"].help_text = None
        if "password1" in self.fields:
            self.fields["password1"].label = "Құпиясөз"
        if "password2" in self.fields:
            self.fields["password2"].label = "Құпиясөзді қайталаңыз"
            self.fields["password2"].help_text = None

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username__iexact=username).exists():
            raise ValidationError("Бұл логин бұрын алынған.")
        return username


class ProfileUpdateForm(forms.ModelForm):
    """Профильді жаңарту: аты-жөні, email, телефон, фото, жұмыс/оқу орны, био."""
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
            "work_place",
            "study_place",
            "bio",
        )
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "avatar" and "class" not in (field.widget.attrs or {}):
                field.widget.attrs["class"] = "form-control"
        if "avatar" in self.fields:
            self.fields["avatar"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].label = "Аты"
        self.fields["last_name"].label = "Тегі"
        self.fields["email"].label = "Email"
        self.fields["phone"].label = "Телефон"
        self.fields["avatar"].label = "Фото"
        self.fields["work_place"].label = "Қайда жұмыс істейді"
        self.fields["study_place"].label = "Қайда оқиды"
        self.fields["bio"].label = "Қысқаша өзі туралы"

