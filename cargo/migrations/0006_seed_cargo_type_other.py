# Data: «Басқа» жүк түрін қосу (қолмен атын жазу үшін)

from django.db import migrations


def add_other(apps, schema_editor):
    CargoType = apps.get_model("cargo", "CargoType")
    CargoType.objects.get_or_create(
        name="Басқа",
        defaults={"category": "other", "price_per_kg": 100, "description": "Жүк атын өзіңіз жазыңыз"},
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("cargo", "0005_seed_route_coordinates"),
    ]

    operations = [
        migrations.RunPython(add_other, noop),
    ]
