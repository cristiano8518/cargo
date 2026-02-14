"""
URL configuration for cargo_project (Карго жеткізу веб-сайты).
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.shortcuts import redirect


def home(request):
    """Үй беті — қош келдіңіз."""
    if request.user.is_authenticated:
        return redirect("users:dashboard")
    return render(request, 'home.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('users/', include('users.urls')),
    path('orders/', include('orders.urls')),
    path('cargo/', include('cargo.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('cargo_project.api_urls')),
]
