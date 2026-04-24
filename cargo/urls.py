from django.urls import path
from . import views

app_name = "cargo"

urlpatterns = [
    path('types/', views.cargo_type_list, name="types"),
    path('routes/', views.route_list, name="routes"),
    path('addresses/', views.addresses_list, name="addresses"),
    path('contact/', views.contact_page, name="contact"),
    path('routes/<int:route_id>/map/', views.route_map_geojson, name="route_map"),
    path('routes/from-points/', views.route_from_points, name="route_from_points"),
    path('routes/set-custom/', views.set_custom_route, name="set_custom_route"),
]
