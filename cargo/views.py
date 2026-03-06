import json
import urllib.request
import urllib.error

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from .models import CargoType, Route

OSRM_BASE = "https://router.project-osrm.org/route/v1/driving"
PRICE_PER_KM = 50  # тг/км — шамалы баға есебі үшін


def cargo_type_list(request):
    qs = CargoType.objects.all()
    q = request.GET.get("q", "")
    if q is None:
        q = ""
    q = str(q).strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    qs = qs.order_by("category", "name")
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "cargo/cargo_type_list.html", {"page_obj": page_obj, "q": q})


def route_list(request):
    qs = Route.objects.all()
    q = request.GET.get("q", "")
    if q is None:
        q = ""
    q = str(q).strip()
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


@require_GET
def route_from_points(request):
    """Екі нүкте бойынша жол геометриясы мен қашықтық (картадан маршрут құру)."""
    try:
        lat1 = float(request.GET.get("lat1"))
        lng1 = float(request.GET.get("lng1"))
        lat2 = float(request.GET.get("lat2"))
        lng2 = float(request.GET.get("lng2"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Координаттар қате (lat1, lng1, lat2, lng2)."}, status=400)
    coords = f"{lng1},{lat1};{lng2},{lat2}"
    url = f"{OSRM_BASE}/{coords}?overview=full&geometries=geojson"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CargoDjango/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
        return JsonResponse({"error": "osrm_error", "message": str(e)}, status=502)
    distance_km = None
    coordinates = [[lat1, lng1], [lat2, lng2]]
    if data.get("code") == "Ok" and data.get("routes"):
        route_data = data["routes"][0]
        distance_m = route_data.get("distance")
        if distance_m is not None:
            distance_km = round(distance_m / 1000, 1)
        geom = route_data.get("geometry", {}).get("coordinates", [])
        if geom:
            coordinates = [[c[1], c[0]] for c in geom]
    else:
        # Түзу сызық қашықтығы (шамамен)
        import math
        R = 6371  # km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lng2 - lng1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        distance_km = round(2 * R * math.asin(math.sqrt(a)), 1)
    estimated_price = (distance_km * PRICE_PER_KM) if distance_km else None
    return JsonResponse({
        "origin": [lat1, lng1],
        "destination": [lat2, lng2],
        "polyline": coordinates,
        "distance_km": distance_km,
        "estimated_price": estimated_price,
        "price_per_km": PRICE_PER_KM,
    })


@login_required
@require_POST
def set_custom_route(request):
    """Картадан құрылған маршрутты сессияға салып, тапсырыс бетіне өту."""
    try:
        origin_lat = float(request.POST.get("origin_lat"))
        origin_lng = float(request.POST.get("origin_lng"))
        dest_lat = float(request.POST.get("dest_lat"))
        dest_lng = float(request.POST.get("dest_lng"))
        distance_km = request.POST.get("distance_km")
        distance_km = float(distance_km) if distance_km else None
    except (TypeError, ValueError):
        return JsonResponse({"error": "Координаттар қате."}, status=400)
    origin_name = (request.POST.get("origin_name") or "").strip() or "Шығу пункті"
    dest_name = (request.POST.get("dest_name") or "").strip() or "Келу пункті"
    request.session["custom_route"] = {
        "origin": origin_name,
        "destination": dest_name,
        "origin_lat": origin_lat,
        "origin_lng": origin_lng,
        "dest_lat": dest_lat,
        "dest_lng": dest_lng,
        "distance_km": distance_km,
    }
    return redirect("orders:create")
