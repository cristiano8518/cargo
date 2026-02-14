from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Пайдаланушы — рөлдер: қарапайым және әкімші."""
    class Role(models.TextChoices):
        USER = 'user', 'Қарапайым пайдаланушы'
        ADMIN = 'admin', 'Әкімші'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Пайдаланушы'
        verbose_name_plural = 'Пайдаланушылар'

    def save(self, *args, **kwargs):
        # Егер superuser/staff болса — рольді автоматты ADMIN қыламыз
        if self.is_superuser or self.is_staff:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)
