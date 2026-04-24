from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cargo.models import CargoType, Route
from orders.models import Order
from users.models import User


class AuthApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="Pass1234!")

    def test_token_obtain_and_me_endpoint(self):
        token_response = self.client.post(
            "/api/auth/token/",
            {"username": "apiuser", "password": "Pass1234!"},
            format="json",
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        access = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        me_response = self.client.get("/api/me/")
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(me_response.data["username"], "apiuser")


class OrdersApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="orders_api", password="Pass1234!")
        self.cargo_type = CargoType.objects.create(name="Тауар", category="tovar", price_per_kg=120)
        self.route = Route.objects.create(origin="Aktau", destination="Oral")

    def test_orders_api_requires_authentication(self):
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_creates_own_order(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/orders/",
            {
                "cargo_type_id": self.cargo_type.id,
                "weight_kg": "5.0",
                "vehicle_type": Order.VehicleType.GAZEL,
                "origin": self.route.origin,
                "destination": self.route.destination,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Order.objects.get(id=response.data["id"])
        self.assertEqual(created.user_id, self.user.id)


class HealthEndpointTests(APITestCase):
    def test_health_endpoint_returns_ok(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], "ok")
