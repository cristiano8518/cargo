from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """Тек тізімнен таңдау: жүк түрі, маршрут, салмақ, көлік, күн. Өзінше жазу жоқ."""
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
        self.fields["cargo_type"].required = True
        self.fields["cargo_type"].empty_label = "— Жүк түрін таңдаңыз —"
        self.fields["cargo_type"].queryset = self.fields["cargo_type"].queryset.order_by("category", "name")
        self.fields["route"].required = True
        self.fields["route"].empty_label = "— Маршрут таңдаңыз —"
        self.fields["route"].queryset = self.fields["route"].queryset.order_by("origin", "destination")
        for name, field in self.fields.items():
            if "class" not in (field.widget.attrs or {}):
                field.widget.attrs.setdefault("class", "form-control")


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

