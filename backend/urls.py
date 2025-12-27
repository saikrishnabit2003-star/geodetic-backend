
from django.urls import path, include
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok", "service": "django-api"})

urlpatterns = [
    path("", health),
    path("stacov/", include("stacov.urls")),
]
