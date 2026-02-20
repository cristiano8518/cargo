# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cargo", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cargotype",
            name="category",
            field=models.CharField(
                choices=[("mal", "Мал"), ("tovar", "Тауарлар")],
                default="tovar",
                max_length=20,
            ),
        ),
        migrations.AlterModelOptions(
            name="cargotype",
            options={"ordering": ["category", "name"], "verbose_name": "Жүк түрі", "verbose_name_plural": "Жүк түрлері"},
        ),
    ]
