# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Фото'),
        ),
        migrations.AddField(
            model_name='user',
            name='work_place',
            field=models.CharField(blank=True, max_length=200, verbose_name='Қайда жұмыс істейді'),
        ),
        migrations.AddField(
            model_name='user',
            name='study_place',
            field=models.CharField(blank=True, max_length=200, verbose_name='Қайда оқиды'),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Қысқаша өзі туралы'),
        ),
    ]
