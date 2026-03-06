from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_order_route_and_blank_origin_dest"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivery_photo",
            field=models.ImageField(
                upload_to="deliveries/",
                null=True,
                blank=True,
                verbose_name="Жеткізу фото",
            ),
        ),
    ]

