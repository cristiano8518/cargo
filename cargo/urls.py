from django.urls import path
from . import views

app_name = "cargo"

urlpatterns = [
    path('types/', views.cargo_type_list, name="types"),
    path('routes/', views.route_list, name="routes"),
]
