from django.urls import path
from . import views

app_name = "cargo"

urlpatterns = [
    path('types/', views.cargo_type_list, name="types"),
    path('routes/', views.route_list, name="routes"),
    path('routes/<int:route_id>/map/', views.route_map_geojson, name="route_map"),
]
