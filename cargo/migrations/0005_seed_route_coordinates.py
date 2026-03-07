# Data: маршруттардың координаттарын толтыру (карта үшін)

from django.db import migrations


# Қала аты -> (latitude, longitude)
CITY_COORDS = {
    "Бишкек": (42.8746, 74.5698),
    "Ош": (40.5301, 72.7985),
    "Жалал-Абад": (40.9333, 73.0),
    "Қара-Балта": (42.8, 73.85),
    "Ташкент": (41.2995, 69.2401),
    "Самарқанд": (39.6542, 66.9597),
    "Бұхара": (39.7680, 64.4556),
    "Наманган": (41.0, 71.67),
    "Андижан": (40.78, 72.34),
    "Алматы": (43.2220, 76.8512),
    "Шымкент": (42.3417, 69.5901),
    "Астана": (51.1694, 71.4491),
    "Қарағанды": (49.8047, 73.0859),
    "Тараз": (42.9, 71.3667),
    "Қызылорда": (44.85, 65.5),
    "Павлодар": (52.2833, 76.95),
    "Қостанай": (53.2144, 63.6246),
}


def fill_coordinates(apps, schema_editor):
    Route = apps.get_model("cargo", "Route")
    for r in Route.objects.all():
        o = CITY_COORDS.get(r.origin.strip())
        d = CITY_COORDS.get(r.destination.strip())
        if o:
            r.origin_lat, r.origin_lng = o
        if d:
            r.destination_lat, r.destination_lng = d
        r.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("cargo", "0004_route_coordinates"),
    ]

    operations = [
        migrations.RunPython(fill_coordinates, noop),
    ]
