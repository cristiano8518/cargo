from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("set-language/", views.set_language_preference, name="set_language"),
    path("guide/", views.guide, name="guide"),
]
