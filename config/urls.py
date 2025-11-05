"""
URL configuration for arte_ideas_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.utils.timezone import now


def api_root(request):
    def abs(url_path: str) -> str:
        return request.build_absolute_uri(url_path)

    return JsonResponse({
        "name": "Arte Ideas API",
        "version": 1,
        "endpoints": {
            "upcoming": abs("/api/crm/agenda/upcoming"),
            "calendar_month": abs("/api/crm/agenda/calendar?view=month&year=2025&month=11"),
            "calendar_week": abs("/api/crm/agenda/calendar?view=week&year=2025&month=11&day=10"),
            "calendar_day": abs("/api/crm/agenda/calendar?view=day&year=2025&month=11&day=10"),
            "healthz": abs("/healthz"),
        }
    })


def healthz(request):
    return JsonResponse({
        "status": "ok",
        "timestamp": now().isoformat(),
        "debug": bool(getattr(settings, "DEBUG", False)),
        "allowed_hosts": getattr(settings, "ALLOWED_HOSTS", []),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/core/', include('apps.core.urls')),
    path('api/crm/', include('apps.crm.urls')),
    path('api/commerce/', include('apps.commerce.urls')),
    path('api/operations/', include('apps.operations.urls')),
    path('api/finance/', include('apps.finance.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    # Raíz informativa y estado de salud
    path('', api_root),
    path('healthz', healthz),
]