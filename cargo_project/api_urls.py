from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.api import MeView
from orders.api import OrderViewSet
from cargo.api import CargoTypeViewSet, RouteViewSet


router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"cargo-types", CargoTypeViewSet, basename="cargo-types")
router.register(r"routes", RouteViewSet, basename="routes")


urlpatterns = [
    # JWT
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Profile
    path("me/", MeView.as_view(), name="me"),
    # Resources
    path("", include(router.urls)),
]

