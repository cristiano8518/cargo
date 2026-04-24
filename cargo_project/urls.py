"""
URL configuration for cargo_project (Карго жеткізу веб-сайты).
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from django.shortcuts import render, redirect

admin.site.site_header = "Карго әкімшілігі"
admin.site.site_title = "Карго"
admin.site.index_title = "Сайт басқаруы"


def home(request):
    """Үй беті — қош келдіңіз."""
    if request.user.is_authenticated:
        return redirect("users:dashboard")
    return render(request, 'home.html')


def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health/", health),
    path('admin/', admin.site.urls),
    path('', home),
    path('users/', include('users.urls')),
    path('orders/', include('orders.urls')),
    path('cargo/', include('cargo.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('cargo_project.api_urls')),
]

# Media files (user uploads) should remain accessible in all environments.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
