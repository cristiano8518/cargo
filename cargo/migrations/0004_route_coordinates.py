# Generated manually: Route coordinates for map

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cargo", "0003_seed_cargo_types_and_routes"),
    ]

    operations = [
        migrations.AddField(
            model_name="route",
            name="origin_lat",
            field=models.FloatField(blank=True, null=True, verbose_name="Шығу пункті (ен)"),
        ),
        migrations.AddField(
            model_name="route",
            name="origin_lng",
            field=models.FloatField(blank=True, null=True, verbose_name="Шығу пункті (ұзындық)"),
        ),
        migrations.AddField(
            model_name="route",
            name="destination_lat",
            field=models.FloatField(blank=True, null=True, verbose_name="Келу пункті (ен)"),
        ),
        migrations.AddField(
            model_name="route",
            name="destination_lng",
            field=models.FloatField(blank=True, null=True, verbose_name="Келу пункті (ұзындық)"),
        ),
    ]
