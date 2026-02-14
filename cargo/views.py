from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import CargoType, Route


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
