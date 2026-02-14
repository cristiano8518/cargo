from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cargo_type', 'weight_kg', 'estimated_price', 'origin', 'destination', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('description', 'origin', 'destination')
