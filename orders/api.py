from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Order
from users.permissions import IsAdminRole


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    cargo_type_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    cargo_type = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj: Order):
        return {"id": obj.user_id, "username": getattr(obj.user, "username", "")}

    def get_cargo_type(self, obj: Order):
        if not obj.cargo_type_id:
            return None
        ct = obj.cargo_type
        return {"id": ct.id, "name": ct.name, "price_per_kg": str(ct.price_per_kg)}

    def validate_user_id(self, value: int):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Аутентификация керек.")
        is_admin = IsAdminRole().has_permission(request, None)
        if not is_admin:
            raise serializers.ValidationError("user_id тек әкімші үшін.")
        User = get_user_model()
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Мұндай user жоқ.")
        return value

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "user_id",
            "cargo_type",
            "cargo_type_id",
            "weight_kg",
            "vehicle_type",
            "estimated_price",
            "description",
            "origin",
            "destination",
            "requested_delivery_date",
            "rejection_reason",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    filterset_fields = ("status",)
    search_fields = ("description", "origin", "destination")
    ordering_fields = ("created_at", "status")
    ordering = ("-created_at",)

    def get_queryset(self):
        # Admin — барлық тапсырыс, user — тек өзінің
        if IsAdminRole().has_permission(self.request, self):
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Admin user_id берсе — соған құрады, әйтпесе өзіндік
        user_id = serializer.validated_data.pop("user_id", None)
        cargo_type_id = serializer.validated_data.pop("cargo_type_id", None)
        from cargo.models import CargoType
        cargo_type = None
        if cargo_type_id:
            cargo_type = CargoType.objects.filter(id=cargo_type_id).first()
        if user_id and IsAdminRole().has_permission(self.request, self):
            User = get_user_model()
            serializer.save(user=User.objects.get(id=user_id), cargo_type=cargo_type)
        else:
            serializer.save(user=self.request.user, cargo_type=cargo_type)

