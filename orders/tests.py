from django.test import TestCase
from django.urls import reverse

from cargo.models import CargoType, Route
from orders.forms import OrderForm
from orders.models import Order
from users.models import User


class OrderFormTests(TestCase):
    def setUp(self):
        self.other_type, _ = CargoType.objects.get_or_create(
            name="Басқа",
            defaults={"category": "other", "price_per_kg": 100},
        )
        self.route = Route.objects.create(origin="Almaty", destination="Astana")

    def test_other_cargo_requires_custom_name(self):
        form = OrderForm(
            data={
                "cargo_type": self.other_type.id,
                "route": self.route.id,
                "weight_kg": "10",
                "vehicle_type": Order.VehicleType.GAZEL,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("custom_cargo_name", form.errors)


class OrderViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="order_user", password="Pass1234!")
        self.cargo_type = CargoType.objects.create(name="Тауар", category="tovar", price_per_kg=150)
        self.route = Route.objects.create(origin="Atyrau", destination="Shymkent")

    def test_order_list_requires_authentication(self):
        response = self.client.get(reverse("orders:list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_authenticated_user_can_create_order(self):
        self.client.login(username="order_user", password="Pass1234!")
        response = self.client.post(
            reverse("orders:create"),
            data={
                "cargo_type": self.cargo_type.id,
                "route": self.route.id,
                "weight_kg": "12.5",
                "vehicle_type": Order.VehicleType.GAZEL,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.filter(user=self.user).count(), 1)
