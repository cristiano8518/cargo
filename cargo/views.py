import json
import urllib.request
import urllib.error

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import CargoType, Route

OSRM_BASE = "https://router.project-osrm.org/route/v1/driving"


def cargo_type_list(request):
    qs = CargoType.objects.all()
    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    qs = qs.order_by("name")
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "cargo/cargo_type_list.html", {"page_obj": page_obj, "q": q})


def route_list(request):
    qs = Route.objects.all()
    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(Q(origin__icontains=q) | Q(destination__icontains=q))
    qs = qs.order_by("origin", "destination")
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "cargo/route_list.html", {"page_obj": page_obj, "q": q})


def route_map_geojson(request, route_id):
    """Маршрут үшін жол геометриясы (картада сызу үшін). OSRM арқылы жол алынады."""
    route = get_object_or_404(Route, pk=route_id)
    if not route.has_coordinates():
        return JsonResponse({
            "error": "no_coordinates",
            "message": "Бұл маршрут үшін координаттар жоқ.",
            "origin": route.origin,
            "destination": route.destination,
        }, status=400)

    # OSRM: координаттар lng,lat ретінде
    coords = f"{route.origin_lng},{route.origin_lat};{route.destination_lng},{route.destination_lat}"
    url = f"{OSRM_BASE}/{coords}?overview=full&geometries=geojson"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CargoDjango/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return JsonResponse({"error": "osrm_error", "message": str(e)}, status=502)
    except (urllib.error.URLError, TimeoutError) as e:
        return JsonResponse({"error": "osrm_error", "message": str(e)}, status=502)

    if data.get("code") != "Ok" or not data.get("routes"):
        # OSRM жол таппаса (мысалы шекара) — түзу сызық көрсетеміз
        coordinates = [
            [route.origin_lat, route.origin_lng],
            [route.destination_lat, route.destination_lng],
        ]
        return JsonResponse({
            "route_id": route.id,
            "origin_name": route.origin,
            "destination_name": route.destination,
            "origin": [route.origin_lat, route.origin_lng],
            "destination": [route.destination_lat, route.destination_lng],
            "polyline": coordinates,
            "distance_km": route.distance_km,
        })

    geometry = data["routes"][0]["geometry"]
    # GeoJSON coordinates are [lng, lat]; Leaflet [lat, lng] күтеді
    coordinates = [[c[1], c[0]] for c in geometry["coordinates"]]

    return JsonResponse({
        "route_id": route.id,
        "origin_name": route.origin,
        "destination_name": route.destination,
        "origin": [route.origin_lat, route.origin_lng],
        "destination": [route.destination_lat, route.destination_lng],
        "polyline": coordinates,
        "distance_km": route.distance_km,
    })
