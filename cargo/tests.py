from django.test import TestCase
from django.urls import reverse

from cargo.models import Route


class CargoViewsTests(TestCase):
    def test_route_from_points_returns_400_for_invalid_input(self):
        response = self.client.get(reverse("cargo:route_from_points"))
        self.assertEqual(response.status_code, 400)

    def test_route_map_requires_coordinates(self):
        route = Route.objects.create(origin="PointA", destination="PointB")
        response = self.client.get(reverse("cargo:route_map", kwargs={"route_id": route.id}))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("error"), "no_coordinates")
