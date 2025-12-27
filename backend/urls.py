
from django.urls import path, include
from django.http import JsonResponse
from stacov import urls

def health(request):
    return JsonResponse({"status": "ok", "service": "django-api"})

urlpatterns = [
    path("", health),
    path("api/", urls),
]
