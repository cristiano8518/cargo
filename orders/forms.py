from django import forms

from cargo.models import CargoType
from .models import Order, Feedback


class OrderForm(forms.ModelForm):
    """Тек тізімнен таңдау: жүк түрі (немесе «Басқа» — өзінше жазу), маршрут, салмақ, көлік, күн."""
    custom_cargo_name = forms.CharField(
        required=False,
        max_length=200,
        label="Жүк аты (өзінше жазыңыз)",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Мысалы: Мысық, Компьютер"}),
    )

    class Meta:
        model = Order
        fields = (
            "cargo_type",
            "route",
            "weight_kg",
            "vehicle_type",
            "requested_delivery_date",
        )
        widgets = {
            "requested_delivery_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CargoType.objects.get_or_create(
            name="Басқа",
            defaults={"category": "other", "price_per_kg": 100, "description": "Жүк атын өзіңіз жазыңыз"},
        )
        self.fields["cargo_type"].required = True
        self.fields["cargo_type"].empty_label = "— Жүк түрін таңдаңыз —"
        self.fields["cargo_type"].queryset = CargoType.objects.all().order_by("category", "name")
        self.fields["route"].required = True
        self.fields["route"].empty_label = "— Маршрут таңдаңыз —"
        self.fields["route"].queryset = self.fields["route"].queryset.order_by("origin", "destination")
        for name, field in self.fields.items():
            if "class" not in (field.widget.attrs or {}):
                field.widget.attrs.setdefault("class", "form-control")

    def clean(self):
        data = super().clean()
        cargo_type = data.get("cargo_type")
        if cargo_type and cargo_type.name == "Басқа":
            custom = (data.get("custom_cargo_name") or "").strip()
            if not custom:
                self.add_error("custom_cargo_name", "«Басқа» таңдағанда жүк атын жазыңыз.")
            else:
                data["custom_cargo_name"] = custom
        return data


class OrderAdminUpdateForm(forms.ModelForm):
    """Әкімші — статус, баға, қабылдамау себебі."""
    class Meta:
        model = Order
        fields = ("status", "estimated_price", "rejection_reason")
        widgets = {
            "rejection_reason": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if "class" not in (field.widget.attrs or {}):
                field.widget.attrs.setdefault("class", "form-control")

    def clean(self):
        data = super().clean()
        if data.get("status") == Order.Status.REJECTED and not (data.get("rejection_reason") or "").strip():
            self.add_error("rejection_reason", "Қабылдамау себебін көрсетіңіз.")
        return data


class FeedbackForm(forms.ModelForm):
    """Пайдаланушы кері байланыс формасы."""

    class Meta:
        model = Feedback
        fields = ("order", "rating", "text", "photo")
        widgets = {
            "order": forms.Select(attrs={"class": "form-select"}),
            "rating": forms.Select(attrs={"class": "form-select"}),
            "text": forms.Textarea(attrs={"rows": 3, "class": "form-control", "placeholder": "Өз пікіріңізді жазыңыз..."}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["order"].queryset = Order.objects.filter(user=user, status=Order.Status.DELIVERED).order_by("-created_at")
            self.fields["order"].required = False
            self.fields["order"].empty_label = "— Тапсырыс таңдау (қаласаңыз) —"
        for name, field in self.fields.items():
            if "class" not in (field.widget.attrs or {}):
                field.widget.attrs.setdefault("class", "form-control")

