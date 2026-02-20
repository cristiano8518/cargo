# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cargo", "0002_cargotype_category"),
        ("orders", "0004_order_vehicle_requested_date_rejection_and_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="route",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to="cargo.route",
                verbose_name="Маршрут",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="description",
            field=models.CharField(blank=True, max_length=500, verbose_name="Сипаттама (авто)"),
        ),
        migrations.AlterField(
            model_name="order",
            name="origin",
            field=models.CharField(blank=True, max_length=200, verbose_name="Қайдан"),
        ),
        migrations.AlterField(
            model_name="order",
            name="destination",
            field=models.CharField(blank=True, max_length=200, verbose_name="Қайда"),
        ),
    ]
