import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update a superuser from environment variables."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Skipping ensure_superuser: DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD is not set."
                )
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if not created:
            changed = False
            if email and user.email != email:
                user.email = email
                changed = True
            if not user.is_staff:
                user.is_staff = True
                changed = True
            if not user.is_superuser:
                user.is_superuser = True
                changed = True
            if changed:
                user.save(update_fields=["email", "is_staff", "is_superuser"])

        user.set_password(password)
        user.save(update_fields=["password"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Superuser '{username}' has been created/updated successfully."
            )
        )
