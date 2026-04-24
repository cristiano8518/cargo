from django.db import models


class CargoType(models.Model):
    """Жүк түрі — тек тізімнен таңдалады (мал, тауарлар)."""
    class Category(models.TextChoices):
        MAL = "mal", "Мал"
        TOVAR = "tovar", "Тауарлар"
        OTHER = "other", "Басқа"

    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.TOVAR,
    )
    description = models.TextField(blank=True)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Жүк түрі"
        verbose_name_plural = "Жүк түрлері"
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class Route(models.Model):
    """Маршрут — шыққан жері мен келу пункті. Карта үшін координаттар."""
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance_km = models.PositiveIntegerField(null=True, blank=True)
    # Картада жол көрсету үшін (OSRM пайдалануға)
    origin_lat = models.FloatField(null=True, blank=True, verbose_name="Шығу пункті (ен)")
    origin_lng = models.FloatField(null=True, blank=True, verbose_name="Шығу пункті (ұзындық)")
    destination_lat = models.FloatField(null=True, blank=True, verbose_name="Келу пункті (ен)")
    destination_lng = models.FloatField(null=True, blank=True, verbose_name="Келу пункті (ұзындық)")

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруттар'

    def __str__(self):
        return f'{self.origin} → {self.destination}'

    def has_coordinates(self):
        return all((
            self.origin_lat is not None, self.origin_lng is not None,
            self.destination_lat is not None, self.destination_lng is not None,
        ))


class ContactMessage(models.Model):
    """Байланыс хабарламалары / пікірлер."""
    name = models.CharField(max_length=120, verbose_name="Аты")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Телефон")
    message = models.TextField(verbose_name="Хабарлама")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Байланыс хабарламасы"
        verbose_name_plural = "Байланыс хабарламалары"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.created_at:%Y-%m-%d %H:%M}"
