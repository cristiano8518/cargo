from django.db import models


class CargoType(models.Model):
    """Жүк түрі — баға және сипаттама."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Жүк түрі'
        verbose_name_plural = 'Жүк түрлері'

    def __str__(self):
        return self.name


class Route(models.Model):
    """Маршрут — шыққан жері мен келу пункті."""
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance_km = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруттар'

    def __str__(self):
        return f'{self.origin} → {self.destination}'
