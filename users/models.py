from django.db import models
from django.contrib.auth.models import AbstractUser


def user_avatar_path(instance, filename):
    return f"avatars/user_{instance.id}/{filename}"


class User(AbstractUser):
    """Пайдаланушы — рөлдер, профиль: фото, жұмыс/оқу орны."""
    class Role(models.TextChoices):
        USER = 'user', 'Қарапайым пайдаланушы'
        ADMIN = 'admin', 'Әкімші'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        verbose_name="Фото",
    )
    work_place = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Қайда жұмыс істейді",
    )
    study_place = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Қайда оқиды",
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Қысқаша өзі туралы",
    )

    class Meta:
        verbose_name = "Пайдаланушы"
        verbose_name_plural = "Пайдаланушылар"

    def save(self, *args, **kwargs):
        if self.is_superuser or self.is_staff:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)
