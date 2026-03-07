from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'cargo_type',
        'route',
        'weight_kg',
        'vehicle_type',
        'estimated_price',
        'origin',
        'destination',
        'requested_delivery_date',
        'status',
        'created_at',
    )
    list_filter = ('status', 'vehicle_type')
    search_fields = ('user__username', 'description', 'origin', 'destination', 'rejection_reason')
    list_per_page = 20
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('Негізгі'), {
            'fields': ('user', 'cargo_type', 'route', 'weight_kg', 'vehicle_type', 'estimated_price', 'description'),
        }),
        (_('Маршрут'), {
            'fields': ('origin', 'destination', 'requested_delivery_date'),
        }),
        (_('Статус'), {
            'fields': ('status', 'rejection_reason'),
        }),
        (_('Уақыт'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['set_status_pending', 'set_status_payment_pending', 'set_status_in_transit', 'set_status_delivered']

    @admin.action(description=_('Статусты: Сұраныс жіберілді'))
    def set_status_pending(self, request, queryset):
        queryset.update(status=Order.Status.PENDING)

    @admin.action(description=_('Статусты: Төлем күтілуде'))
    def set_status_payment_pending(self, request, queryset):
        queryset.update(status=Order.Status.PAYMENT_PENDING)

    @admin.action(description=_('Статусты: Жолда'))
    def set_status_in_transit(self, request, queryset):
        queryset.update(status=Order.Status.IN_TRANSIT)

    @admin.action(description=_('Статусты: Жеткізілді'))
    def set_status_delivered(self, request, queryset):
        queryset.update(status=Order.Status.DELIVERED)
