from django.contrib import admin
<<<<<<< HEAD
from .models import CargoType, Route, ContactMessage
=======
from .models import CargoType, Route
>>>>>>> 8a46089c6e4ac2488b9ba8f7e0d529c789420f11


@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_per_kg', 'description_short')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('category', 'name')
    list_per_page = 25

    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + '…' if len(obj.description) > 50 else obj.description
        return '—'

    description_short.short_description = 'Сипаттама'


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'distance_km', 'has_coordinates')
    search_fields = ('origin', 'destination')
    ordering = ('origin', 'destination')
    list_per_page = 25
    fieldsets = (
        (None, {'fields': ('origin', 'destination', 'distance_km')}),
        ('Карта (координаттар)', {
            'fields': ('origin_lat', 'origin_lng', 'destination_lat', 'destination_lng'),
            'description': 'Жол картада көрсетілуі үшін толтырыңыз. Бос қалдырсаңыз, seed миграция толтырады.',
        }),
    )
<<<<<<< HEAD


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
=======
>>>>>>> 8a46089c6e4ac2488b9ba8f7e0d529c789420f11
