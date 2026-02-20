# Generated manually for new order flow

from django.db import migrations, models


def status_old_to_new(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    Order.objects.filter(status="new").update(status="pending")
    Order.objects.filter(status="confirmed").update(status="accepted")


def status_new_to_old(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    Order.objects.filter(status="pending").update(status="new")
    Order.objects.filter(status="accepted").update(status="confirmed")


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_order_cargo_type_order_estimated_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="vehicle_type",
            field=models.CharField(
                choices=[
                    ("gazel", "Газель"),
                    ("kamaz", "Камаз"),
                    ("tral", "Трал"),
                    ("other", "Басқа"),
                ],
                default="gazel",
                max_length=20,
                verbose_name="Көлік түрі",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="requested_delivery_date",
            field=models.DateField(blank=True, null=True, verbose_name="Жеткізу күні"),
        ),
        migrations.AddField(
            model_name="order",
            name="rejection_reason",
            field=models.TextField(blank=True, verbose_name="Қабылдамау себебі"),
        ),
        migrations.AlterField(
            model_name="order",
            name="description",
            field=models.CharField(max_length=500, verbose_name="Не тасымалдау керек"),
        ),
        migrations.AlterField(
            model_name="order",
            name="origin",
            field=models.CharField(max_length=200, verbose_name="Қайдан (адрес)"),
        ),
        migrations.AlterField(
            model_name="order",
            name="destination",
            field=models.CharField(max_length=200, verbose_name="Қайда жеткізу (адрес)"),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Сұраныс жіберілді"),
                    ("accepted", "Қабылданды"),
                    ("rejected", "Қабылданбады"),
                    ("payment_pending", "Төлем күтілуде"),
                    ("paid", "Төленді"),
                    ("in_transit", "Жолда"),
                    ("delivered", "Жеткізілді"),
                    ("cancelled", "Бас тартылды"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.RunPython(status_old_to_new, status_new_to_old),
    ]
