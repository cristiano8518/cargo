from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny

from .models import CargoType, Route


class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = ("id", "name", "description", "price_per_kg")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "origin", "destination", "distance_km")


class CargoTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CargoType.objects.all().order_by("name")
    serializer_class = CargoTypeSerializer
    permission_classes = [AllowAny]
    search_fields = ("name", "description")
    ordering_fields = ("name", "price_per_kg")


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.all().order_by("origin", "destination")
    serializer_class = RouteSerializer
    permission_classes = [AllowAny]
    search_fields = ("origin", "destination")
    ordering_fields = ("origin", "destination", "distance_km")

