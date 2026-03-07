from django.db import models
from django.conf import settings


class Order(models.Model):
    """Тапсырыс — карго жеткізу."""
    class Status(models.TextChoices):
        PENDING = "pending", "Сұраныс жіберілді"
        ACCEPTED = "accepted", "Қабылданды"
        REJECTED = "rejected", "Қабылданбады"
        PAYMENT_PENDING = "payment_pending", "Төлем күтілуде"
        PAID = "paid", "Төленді"
        IN_TRANSIT = "in_transit", "Жолда"
        DELIVERED = "delivered", "Жеткізілді"
        CANCELLED = "cancelled", "Бас тартылды"

    class VehicleType(models.TextChoices):
        GAZEL = "gazel", "Газель"
        KAMAZ = "kamaz", "Камаз"
        TRAL = "tral", "Трал"
        OTHER = "other", "Басқа"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    cargo_type = models.ForeignKey(
        "cargo.CargoType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Жүк түрі",
    )
    route = models.ForeignKey(
        "cargo.Route",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Маршрут",
    )
    weight_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Салмақ (кг)",
    )
    vehicle_type = models.CharField(
        max_length=20,
        choices=VehicleType.choices,
        default=VehicleType.GAZEL,
        verbose_name="Көлік түрі",
    )
    estimated_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Есептелген баға",
    )
    description = models.CharField(max_length=500, blank=True, verbose_name="Сипаттама (авто)")
    origin = models.CharField(max_length=200, blank=True, verbose_name="Қайдан")
    destination = models.CharField(max_length=200, blank=True, verbose_name="Қайда")
    requested_delivery_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Жеткізу күні",
    )
    rejection_reason = models.TextField(
        blank=True,
        verbose_name="Қабылдамау себебі",
    )
    delivery_photo = models.ImageField(
        upload_to="deliveries/",
        null=True,
        blank=True,
        verbose_name="Жеткізу фото",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_seen = models.BooleanField(default=False, verbose_name="Админ көрді")

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


class Feedback(models.Model):
    """Пайдаланушының кері байланысы / отзывы."""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="feedbacks",
        verbose_name="Тапсырыс (қаласаңыз)",
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        default=5,
        verbose_name="Баға (1–5 жұлдыз)",
    )
    text = models.TextField(verbose_name="Отзыв мәтіні")
    photo = models.ImageField(
        upload_to="feedback/",
        null=True,
        blank=True,
        verbose_name="Фото (қаласаңыз)",
    )
    admin_reply = models.TextField(
        blank=True,
        verbose_name="Әкімші жауабы",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Кері байланыс"
        verbose_name_plural = "Кері байланыстар"
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} feedback by {self.user}"
