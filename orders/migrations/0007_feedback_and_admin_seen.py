from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0006_order_delivery_photo"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="admin_seen",
            field=models.BooleanField(default=False, verbose_name="Админ көрді"),
        ),
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField(choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")], default=5, verbose_name="Баға (1–5 жұлдыз)")),
                ("text", models.TextField(verbose_name="Отзыв мәтіні")),
                ("photo", models.ImageField(blank=True, null=True, upload_to="feedback/", verbose_name="Фото (қаласаңыз)")),
                ("admin_reply", models.TextField(blank=True, verbose_name="Әкімші жауабы")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("order", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="feedbacks", to="orders.order", verbose_name="Тапсырыс (қаласаңыз)")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="feedbacks", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Кері байланыс",
                "verbose_name_plural": "Кері байланыстар",
                "ordering": ["-created_at"],
            },
        ),
    ]

