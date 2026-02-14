from django.db import models
from django.conf import settings


class Order(models.Model):
    """Тапсырыс — карго жеткізу."""
    class Status(models.TextChoices):
        NEW = 'new', 'Жаңа'
        CONFIRMED = 'confirmed', 'Расталды'
        IN_TRANSIT = 'in_transit', 'Жолда'
        DELIVERED = 'delivered', 'Жеткізілді'
        CANCELLED = 'cancelled', 'Бас тартылды'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    cargo_type = models.ForeignKey(
        "cargo.CargoType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Жүк түрі",
    )
    weight_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Салмақ (кг)",
    )
    estimated_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Есептелген баға",
    )
    description = models.CharField(max_length=500)
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Тапсырыс'
        verbose_name_plural = 'Тапсырыстар'
        ordering = ['-created_at']

    def recalc_estimated_price(self):
        if self.cargo_type and self.weight_kg is not None:
            return self.weight_kg * self.cargo_type.price_per_kg
        return 0

    def save(self, *args, **kwargs):
        self.estimated_price = self.recalc_estimated_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'#{self.pk} {self.origin} → {self.destination}'
